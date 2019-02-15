title: 记一次使用RxJava重构的经历
date: 2015-12-21 08:55:29
tags: [Android,Java,RxJava]
categories: 前端
toc: true
---

## 前言

垃圾代码时常会出现在时间不够的情况下，所以重构是一件非常重要非常有意义的事情。

## 需求

我们的 **[Studio](https://github.com/XhinLiang/Studio)** 项目中需要上传头像的功能，所以选择了一个开源库 [PhotoPicker](https://github.com/donglua/PhotoPicker) 来做图片的选择。通过这个库我们就可以在**Activity # onActivityResult** 方法来获取用户选择的图片地址，然后通过 [LeanCloud](https://leancloud.cn/) 的 **AVFile** 来进行上传。

## 原来的实现

```
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    super.onActivityResult(requestCode, resultCode, data);
    if (resultCode != RESULT_OK)
        return;
    if (requestCode != 1 || data == null)
        return;
    String photo = data.getStringArrayListExtra(PhotoPickerActivity.KEY_SELECTED_PHOTOS).get(0);
    AVFile file = null;
    try {
        file = AVFile.withAbsoluteLocalPath(String.format("avatar_%s.jpg", user.name), photo);
    } catch (IOException e) {
        e.printStackTrace();
    }
    if (file == null)
        return;
    final ProgressDialog pd = new ProgressDialog(this);
    pd.setMax(100);
    pd.show();
    final AVFile finalFile = file;
    file.saveInBackground(new SaveCallback() {
        @Override
        public void done(AVException e) {
            pd.hide();
            if (e != null) {
                showSimpleDialog(R.string.error);
                return;
            }
            user.imgurl = finalFile.getUrl();
            observableUpdate.subscribe(observerUser);
        }
    }, new ProgressCallback() {
        @Override
        public void done(Integer integer) {
            pd.setProgress(integer);
        }
    });
}
```


## 存在的问题

*原先的这段代码事实上是可以用的，运行起来也没有什么问题，但是作为代码洁癖患者，我们还是可以挑出刺来*
- 在主线程进行 **IO操作** ，影响用户体验。
- **IO** 操作有 **Checked异常** ，但是在代码中捕获异常后代码变得非常难看。 

**最让我不能忍的莫过于这段**

```
AVFile file = null;
try {
    file = AVFile.withAbsoluteLocalPath(String.format("avatar_%s.jpg", user.name), photo);
} catch (IOException e) {
    e.printStackTrace();
}
if (file == null)
    return;
final ProgressDialog pd = new ProgressDialog(this);
pd.setMax(100);
pd.show();
final AVFile finalFile = file;
```
由于 **AVFile** 的 **withAbsoluteLocalPath** 方法有 **Checked** 异常，在调用的时候必须捕获异常，然而在上传头像 （**AVFile** 的 **saveInBackgroud** 方法）中，我们需要更新用户的 **头像URL** 而需要使用到这个 **AVFile** 对象，所以我们还得在定义一个 **final** 对象！

```
final AVFile finalFile = file;
```
#### 多么蛋疼！！！

## 解决办法

事实上我们根据 **RxJava** “流”的概念可以想到，这一大串代码，事实上也可以化为一个”流“，而这个”流“就是从我们获取的头像的本地地址开始的。

然后接下来的代码都很简单了

```
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    super.onActivityResult(requestCode, resultCode, data);
    if (resultCode != RESULT_OK || requestCode != REQUEST_FOR_SELECT_PICTURE || data == null)
        return;
    String photo = data.getStringArrayListExtra(PhotoPickerActivity.KEY_SELECTED_PHOTOS).get(0);
    Observable.just(photo)
            .subscribeOn(Schedulers.io())
            .observeOn(Schedulers.io())
            .map(new Func1<String, AVFile>() {
                @Override
                public AVFile call(String s) {
                    try {
                        return AVFile.withAbsoluteLocalPath(String.format("avatar_%s_%d.jpg", user.name, System.currentTimeMillis()), s);
                    } catch (IOException e) {
                        return null;
                    }
                }
            })
            .observeOn(AndroidSchedulers.mainThread())
            .filter(new Func1<AVFile, Boolean>() {
                @Override
                public Boolean call(AVFile avFile) {
                    if (avFile == null) {
                        showSimpleDialog(R.string.can_not_find_file);
                        return false;
                    }
                    return true;
                }
            })
            .compose(this.<AVFile>bindToLifecycle())
            .subscribe(new Action1<AVFile>() {
                @Override
                public void call(final AVFile file) {
                    final ProgressDialog pd = new ProgressDialog(MyDetailsActivity.this);
                    pd.setMax(100);
                    pd.show();
                    file.saveInBackground(new SaveCallback() {
                        @Override
                        public void done(AVException e) {
                            pd.hide();
                            if (e != null) {
                                showSimpleDialog(R.string.error);
                                return;
                            }
                            user.imgurl = file.getUrl();
                            observableUpdate.subscribe(observerUser);
                        }
                    }, new ProgressCallback() {
                        @Override
                        public void done(Integer integer) {
                            pd.setProgress(integer);
                        }
                    });
                }
            });
}
```


使用了 **RxJava**，我们的代码变得非常清晰，也比原来的代码优雅了很多。更重要的是，我们通过 **RxJava** 的 **线程控制** ，把 **IO操作** 真正放到了 **IO线程** 中，主线程不受影响，界面依旧流畅。

## 超越重构
*维基百科上对于 ”重构“ 一词的解释如下*

> 代码重构（英语：Code refactoring）指对软件代码做任何更动以增加可读性或者简化结构而不影响输出结果。 

**对于这一段代码，我们要做的重构工作已经完成，然而还有一些小问题**

- 进度条没有显示
- 没有对上传的图片进行压缩

其实第一条很简单，只需把 **ProgressDialog** 的样式改为水平即可

```
final ProgressDialog pd = new ProgressDialog(MyDetailsActivity.this);
pd.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
pd.setMax(100);
pd.show();
```
第二条改起来也简单，我们根据用户选择的图片找到这个文件，读入为 **Bitmap** ，然后获取它的**原始宽高**，然后再根据它**原始宽高**的大小判断是否需要进行压缩（我们只进行尺寸压缩，不进行质量压缩），这里我们选择 **1000px** 作为临界值，如果宽度或者高度有一个大于 **1000px** 则对宽高进行等比例压缩。

 **完整代码如下**

```
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    super.onActivityResult(requestCode, resultCode, data);
    if (resultCode != RESULT_OK || requestCode != REQUEST_FOR_SELECT_PICTURE || data == null)
            return;
    //因为设置了PhotoPicker只能选择一个图片，所以这里只选取List的第一个元素
    String photo = data.getStringArrayListExtra(PhotoPickerActivity.KEY_SELECTED_PHOTOS).get(0);
    //这一段IO处理事实上是耗时的，但又没有到达需要加上等待动画的地步
    Observable.just(photo)
            .subscribeOn(Schedulers.io())
            .observeOn(Schedulers.io())
            .map(new Func1<String, File>() {
                @Override
                public File call(String filePath) {
                    Bitmap bitmap = compressImageByPixel(filePath, 1000);
                    String uploadName = String.format("avatar_%s_%d", user.name, System.currentTimeMillis());
                    File file = new File(getFilesDir().getAbsolutePath(), uploadName);
                    try {
                        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, new FileOutputStream(file));
                    } catch (FileNotFoundException e) {
                        return null;
                    } finally {
                        bitmap.recycle();
                    }
                    return file;
                }
            })
            .map(new Func1<File, AVFile>() {
                @Override
                public AVFile call(File compressFile) {
                    try {
                        return AVFile.withFile(compressFile.getName(), compressFile);
                    } catch (IOException e) {
                        return null;
                    }
                }
            })
            .observeOn(AndroidSchedulers.mainThread())
            .filter(new Func1<AVFile, Boolean>() {
                @Override
                public Boolean call(AVFile avFile) {
                    if (avFile == null) {
                        showSimpleDialog(R.string.can_not_find_file);
                        return false;
                    }
                    return true;
                }
            })
            .compose(this.<AVFile>bindToLifecycle())//这里用了RxLifeCycle来管理Subscription
            .subscribe(new Action1<AVFile>() {
                @Override
                public void call(final AVFile file) {
                    final ProgressDialog pd = new ProgressDialog(MyDetailsActivity.this);
                    pd.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
                    pd.setMax(100);
                    pd.show();
                    file.saveInBackground(new SaveCallback() {
                        @Override
                        public void done(AVException e) {
                            pd.dismiss();
                            if (e != null) {
                                showSimpleDialog(R.string.error, e.getMessage());
                                return;
                            }
                            user.imgurl = file.getUrl();
                            observableUpdate.subscribe(observerUser);
                        }
                    }, new ProgressCallback() {
                        @Override
                        public void done(Integer integer) {
                            pd.setProgress(integer);
                        }
                    });
                }
            });
}

public Bitmap compressImageByPixel(String imgPath, int maxSize) {
    BitmapFactory.Options newOpts = new BitmapFactory.Options();
    newOpts.inJustDecodeBounds = true;//只读边,不读内容
    BitmapFactory.decodeFile(imgPath, newOpts);
    newOpts.inJustDecodeBounds = false;
    int scale = 1;
    //缩放比,用高或者宽其中较大的一个数据进行计算
    if (newOpts.outWidth > newOpts.outHeight && newOpts.outWidth > maxSize) {
        scale = newOpts.outWidth / maxSize;
    }
    if (newOpts.outWidth < newOpts.outHeight && newOpts.outWidth > maxSize) {
        scale = newOpts.outHeight / maxSize;
    }
    scale++;
    newOpts.inSampleSize = scale;//设置采样率
    return BitmapFactory.decodeFile(imgPath, newOpts);
}
```


## 后记
 **[Studio](https://github.com/XhinLiang/Studio)** 是我很用心写的一个应用，代码已经尽我能力进行了优化，如果大家有时间不妨到看看源代码，欢迎大家 **PR** 。

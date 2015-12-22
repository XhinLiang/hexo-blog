title: RxJava && Retrofit 简化RESTful请求
date: 2015-12-3 16:55:29
tags: [Android]
categories: Android
toc: true
---

>![](./uploads/avatar.png)

## 前言

最近抽空了解了RxJava && Retrofit 这两个库，然后正好我所在的[微客工作室](wecanstudio.me)要写个签到的App。于是乎把最近学到的好玩的东西都加上了，恰逢博客开张，写篇博文庆祝一下。

## 简介

1. [RxJava](https://github.com/ReactiveX/RxJava)
   > 一个在 Java VM 上使用可观测的序列来组成异步的、基于事件的程序的库

2. [Retrofit](https://square.github.io/retrofit)
   > 一个 Android 平台上的类型安全的 REST 客户端。

## 推荐教程

- [给 Android 开发者的 RxJava 详解](http://gank.io/post/560e15be2dca930e00da1083)
- [用 Retrofit 2 简化 HTTP 请求](https://realm.io/cn/news/droidcon-jake-wharton-simple-http-retrofit-2/)

## 准备工作
1. 添加依赖
 

```
    compile 'io.reactivex:rxjava:1.0.14' 
    compile 'io.reactivex:rxandroid:1.0.1'
    compile 'com.google.code.gson:gson:2.4'
    compile 'com.squareup.okhttp:okhttp:2.5.0'
    compile 'com.squareup.retrofit:retrofit:2.0.0-beta2'
    compile 'com.squareup.retrofit:converter-gson:2.0.0-beta2'
    compile 'com.squareup.retrofit:adapter-rxjava:2.0.0-beta2'
    compile 'com.trello:rxlifecycle:0.3.0'
    compile 'com.trello:rxlifecycle-components:0.3.0'
    compile 'com.jakewharton.rxbinding:rxbinding-support-v4:0.2.0'
    compile 'com.jakewharton.rxbinding:rxbinding-appcompat-v7:0.2.0'
    compile 'com.jakewharton.rxbinding:rxbinding-design:0.2.0'
```

 **看到这么多的依赖，大家不要慌张。其实有很多只是同一个库的不同版本，例如RxBinding这个库就对Support-v4 AppCompat-v7 等四个包做了匹配，如果你的项目中没有使用Design包或者你不需要做Design包控件的RxBinding，你也就不需要添加最后一行的依赖**
2. 阅读[接口文档](https://github.com/XhinLiang/Studio/blob/master/Api.md)

 **我们可以看到这些接口都是典型的RESTful接口这也正中Retrofit的下怀，时间和精力有限，我就只拿登录这个个接口举例，剩余的代码大家如果感兴趣可以去看[源代码](https://github.com/XhinLiang/Studio)**

## 正式开始

1. 写Api接口
   

```
public interface Api {
    String BASE_URL = "http://121.42.209.19/RestfulApi/index.php/";
    @GET("api/users")
    Observable<User> login(@Query("name") String name, @Query("phone") String phone);
    //...MORE...
}
```

 **因为我们要使用RxJava的Observable来处理数据，所以定义的时候写上Observable的泛型即可**
2. 写POJO,事实上就是第一步里面出现的 **User**，**BaseData** , **RegisterBody**

```
public class User {
    public int position;
    public int group_name;
    public int id;
    public int sex;
    public int status;
    public String phone;
    public String sign_date;
    public String name;
    public String imgurl;
    public String description;
    public static final String[] groups = {
            "组别", "前端", "后台", "移动", "产品", "设计", "YOU KNOW NOTHING"
    };
    public static final String[] positions = {
            "职位", "组员", "组长", "室长", "John Snow"
    };
    public static final String[] sexs = {
            "性别", "男", "女"
    };
    public static final int VALUE_STATUS_SIGN = 1;
    public static final int VALUE_STATUS_UNSIGN = 0;
}
```

**这里篇幅有限，贴出来的代码可能有所简化，如果大家有时间不妨去看看源代码**

3. 在Application中进行初始化
    
```
public void onCreate() {
    super.onCreate();
    OkHttpClient okHttpClient = new OkHttpClient();
    //OKHttp的使用
    okHttpClient.networkInterceptors().add(new Interceptor() {
        @Override
        public Response intercept(Chain chain) throws IOException {
            return chain.proceed(chain.request().newBuilder()
                    .header(KEY_BUILD_VERSION, BuildConfig.VERSION_NAME)
                    .build());
        }
    });
    //初始化Gson
    Gson gson = new GsonBuilder()
        .setFieldNamingPolicy(FieldNamingPolicy.LOWER_CASE_WITH_UNDERSCORES)
            .setDateFormat(DATE_FORMAT_PATTERN)
            .create();
    //初始化Retrofit
    retrofit = new Retrofit.Builder()
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create(gson))
            .addCallAdapterFactory(RxJavaCallAdapterFactory.create())
            .baseUrl(Api.BASE_URL)
            .build();
}
//返回Retrofit的API
public <T> T createApi(Class<T> service) {
    if (!apis.containsKey(service)) {
        T instance = retrofit.create(service);
        apis.put(service, instance);
    }
    //noinspection unchecked
    return (T) apis.get(service);
}
```

**同时Application对外提供静态实例和 Retrofit 实例的Getter（代码略）**

4. 在Activity中获取 **Api** 并绑定点击事件

```
protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = DataBindingUtil.setContentView(this, R.layout.activity_login);
        setSupportActionBar(binding.toolbar);
        api = App.from(this).createApi(Api.class);
        ProgressDialog pd = new ProgressDialog(this);
        Observable.Transformer<User, User> networkingIndicator = RxNetworking.bindConnecting(pd);
        binding.setName(PreferenceHelper.getInstance(this).getString(App.KEY_PREFERENCE_USER, getString(R.string.nothing)));
        binding.setPhone(PreferenceHelper.getInstance(this).getString(App.KEY_PREFERENCE_PHONE, getString(R.string.nothing)));
        observableConnect = Observable
                //defer操作符是直到有订阅者订阅时，才通过Observable的工厂方法创建Observable并执行
                //defer操作符能够保证Observable的状态是最新的
                .defer(new Func0<Observable<User>>() {
                    @Override
                    public Observable<User> call() {
                        return api.login(binding.etName.getText().toString(), binding.etPhone.getText().toString());
                    }
                })
                .subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .compose(networkingIndicator);
        RxView.clickEvents(binding.btnLogin)
                .filter(new EditTextFilter(binding.etName, R.string.name_no_input))
                .filter(new EditTextFilter(binding.etPhone, R.string.phone_no_input))
                .compose(this.<ViewClickEvent>bindToLifecycle())
                .subscribe(new Action1<ViewClickEvent>() {
                    @Override
                    public void call(ViewClickEvent viewClickEvent) {
                        login();
                    }
                });
        setRxClick(binding.btnRegister)
                .compose(this.<ViewClickEvent>bindToLifecycle())
                .subscribe(new Action1<ViewClickEvent>() {
                    @Override
                    public void call(ViewClickEvent viewClickEvent) {
                        startActivity(new Intent(LoginActivity.this, RegisterActivity.class));
                    }
                });
        setupUmengUpdate();
    }
    private void login() {
        observableConnect
                .compose(this.<User>bindToLifecycle())
                .subscribe(new Action1<User>() {
                    @Override
                    public void call(User user) {
                        PreferenceHelper.getInstance(LoginActivity.this).saveParam(App.KEY_PREFERENCE_USER, binding.etName.getText().toString());
                        PreferenceHelper.getInstance(LoginActivity.this).saveParam(App.KEY_PREFERENCE_PHONE, binding.etPhone.getText().toString());
                        startActivity(new Intent(LoginActivity.this, MainActivity.class).putExtra(MainActivity.KEY_USER, user));
                        finish();
                    }
                }, new Action1<Throwable>() {
                    @Override
                    public void call(Throwable throwable) {
                        //事实上在code != 200 的时候 , 可以获取响应的body.
                        if (throwable instanceof HttpException){
                            try {
                                showSimpleDialog(R.string.login_fail, ((HttpException) throwable).response().errorBody().string());
                            } catch (IOException e) {
                                showSimpleDialog(R.string.login_fail,throwable.getMessage());
                            }
                            return;
                        }
                        showSimpleDialog(R.string.login_fail,throwable.getMessage());
                    }
                });
    }
```

**在博客里总是不适合贴那么多代码的，或者说我的组织能力太差了，贴出来的代码完全不知所云。如果大家有兴趣，还请大家到我的GitHub逛一逛**





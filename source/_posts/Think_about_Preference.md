title: Android™ 中设置界面的思考
date: 2016-3-11 11:55:29
tags: [Android]
categories: Android
toc: true
---

### 引言
在 **Android™** 中大部分应用都需要一个 **系统设置** 界面，有很多开发者（或者开发组）都喜欢自己做一个 **Activity** 或者 **Fragment** 作为设置界面。但是谷歌本来就为 **Android™** 的设置界面提供了一个解决方案，那就是 **PreferenceFragment**（PreferenceActivity 已经不推荐使用）。

遗憾的是，由于 **Android™** 设备的碎片化，同样的代码，在不同的 **API** 中会有相当大的界面区别。

### 原生库
如下的 **PreferenceScreen** 的 **XML** 代码
``` xml
<?xml version="1.0" encoding="utf-8"?>
<PreferenceScreen xmlns:android="http://schemas.android.com/apk/res/android">
    <PreferenceCategory android:title="Alert Settings">
        <CheckBoxPreference
            android:key="preference_key_remind_the_same_day11"
            android:summary="Alert in the birthday"
            android:title="Alert first" />
        <SwitchPreference
            android:key="preference_key_remind_the_same_day31"
            android:summary="Alert in three day before birthday"
            android:title="Alert second" />
        <EditTextPreference
            android:key="preference_key_remind_the_same_daywwwd21"
            android:summary="Alert in a week before the birthday"
            android:title="Alert third" />
        <SwitchPreference
            android:key="preference_key_remind_the_same_day341"
            android:summary="Alert in two weeks before the birthday"
            android:title="Alert fourth" />
        <ListPreference
            android:entries="@array/alert_time_entry"
            android:entryValues="@array/alert_time_value"
            android:key="preference_key_alert_timess1"
            android:summary="Select alert time"
            android:title="Alert time"/>
        <MultiSelectListPreference
            android:entries="@array/alert_time_entry"
            android:entryValues="@array/alert_time_value"
            android:key="preference_key_alert_timeddwexss1"
            android:summary="Select alert time"
            android:title="Alert time" />
    </PreferenceCategory>

</PreferenceScreen>
```

在不同设备的效果如图所示
![original](/uploads/Think_about_Preference/original_preference.gif)

左边的是 **API 16 Android™ 4.1.1**，右边的是 **API 22 Android™ 5.1.1**

也正是因为效果差别如此之大，所以使用系统的 **Preference** 并不是一个很好的选择。

### 解决方案
最近实习的公司也基本敲定了，也有空搞点有趣的东西，结合 [Android-MaterialPreference](https://github.com/jenzz/Android-MaterialPreference) 和 [material](https://github.com/rey5137/material) 这两个第三方的 **Material Design** 兼容库，组合出来一个便于使用的 [MDPreference](https://github.com/XhinLiang/MDPreference)。

#### 引入
在项目的主 build.gradle 中添加 **jitpack** 的仓库

``` groovy
allprojects {
    repositories {
	...
	maven { url "https://jitpack.io" }
    }
}
```
添加依赖
``` groovy
dependencies {
    compile 'com.github.XhinLiang.MDPreference:mdpreference:0.3.1@aar'
    // You should add this because the 'mdpreference' depend on this
    compile 'com.github.XhinLiang.MDPreference:material:0.3.1@aar'
    // You should add these because the 'material' depend on them
    compile 'com.android.support:appcompat-v7:23.1.1'
    compile 'com.android.support:cardview-v7:23.1.1'
    compile 'com.android.support:recyclerview-v7:23.1.1'
}
```
这里还得说明一下
``` groovy
compile 'com.github.XhinLiang.MDPreference:material:0.3.1@aar'
```
这个依赖也必须添加，因为里面很多控件都是使用了 [material](https://github.com/rey5137/material) 这个库，为什么不直接添加这个库本身的依赖，是因为这个库里面的接口有点乱，添加的是我重构删减过的版本。

#### 效果
这里展示了在 **API 16** 设备中的效果
![sample](/uploads/Think_about_Preference/sample.gif)

对话框变色应该是截图软件引起的

#### 使用
事实上这个库的使用跟 **Android™** 官方的没什么区别，有区别的地方在 **ListPreference** 和 **MultiSelectListPreference**。由于官方的 **entries entryValues** 这两个资源ID是私有的，所以只好自己另外定义资源ID。

对于 **ListPreference**，具体是这个样子的
``` xml
<io.github.xhinliang.mdpreference.ListPreference
    android:key="preference_key_alert_timess"
    android:summary="Select alert time"
    android:title="Alert time"
    app:entry_arr="@array/alert_time_entry"
    app:format_str="%s"
    app:value_arr="@array/alert_time_value" />
```
其中  **entry_arr** 是展示给用户的那个数组，

 **format_str** 就是一个 **summary** 的输出格式，它里面的 **%s** 在输出时会被替换为选择的那个 **entry**。例如
``` xml
app:format_str="The Alert Time is %s"
```
在用户选择之前，**Summary** 为 "Select alert time"，而在用户选择了 "12:00" 之后，**Summary** 为 "The Alert Time is 12:00"。

而 **value_arr** 则是我们获取到的值的数组。也就是说，在用户选择了一个 **entry** 之后，我们通过 **SharePreference** 获取到的那个 **String** 的值，这其实跟官方的思路是一模一样的。

示例代码如下
``` java
SharedPreferences preferences = getSharedPreferences(getString(R.string.app_name), MODE_PRIVATE);
preferences.getString("preference_key_alert_timess", "");
```

对于 **MultiSelectListPreference**，具体是这个样子的

``` xml
<io.github.xhinliang.mdpreference.MultiSelectListPreference
    android:key="preference_key_alert_timeddwexss"
    android:summary="Select alert time"
    android:title="Alert time"
    app:entry_arr="@array/alert_time_entry" />
```
注意这里跟官方的差别有点大，其中  **entry_arr** 是展示给用户的那个数组，而 **value_arr** 这个参数被我砍掉了。因为我觉得像官方一样把整个 **value String** 集合保存在 **SharePreference** 里是十分不优雅的。

我选择了另一种方式，将用户选择的 **entry** 的下标用 **int** 保存起来。

也就是说，在用户选择了一个 **entry** 之后，我们只能通 **SharePreference** 获取到的一个 **int** ，这个 **int** 的每一个二进制位的 **0** 或 **1** 就代表了对应下标的选项的选择与否，为了减少二进制操作的麻烦，这里还提供了一个静态方法 **MultiSelectListPreference.getSetByBit** 可以将获得的 **int** 转换为对应的 **Set** ，这个 **Set** 里面包含了被选中的选项的下标。

示例代码如下
``` java
int bit = preferences.getInt("key_multi",0);
Set<Integer> set = MultiSelectListPreference.getSetByBit(bit);
```

### 思考
为什么在官方的实现里要使用 **entry + value** 这样的方案呢，事实上使用下标来代表是否选择，不是更加优雅吗？（事实上我有想把 **ListPreference** 里的方案也改掉的冲动）

这只是我个人的看法，如有错误欢迎指出。



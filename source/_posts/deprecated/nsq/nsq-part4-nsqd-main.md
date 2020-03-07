title: 理解 Nsq （四）源码解析
date: 2018-12-4
tags: [nsq,消息队列,messageQueue,go,golang]
categories: 后端
toc: true
---

## Overview

上一节我们介绍了 Nsq 的一些基本概念，那么我们从这节开始就单刀直入 Nsq 源码探个究竟。

本节先看 nsqd 的入口源代码文件 `nsq/apps/nsqd.go`

先看 main 方法吧：

``` go
func main() {
	prg := &program{}
	if err := svc.Run(prg, syscall.SIGINT, syscall.SIGTERM); err != nil {
		log.Fatal(err)
	}
}
```

其实 main 方法很简单，就是把整个程序交给了 go-svc 这个库，然后由 go-svc 这个库来管理自己的生命周期。

svc.Run 的 Service 需要实现下面三个接口：

``` go
// Service interface contains Start and Stop methods which are called
// when the service is started and stopped. The Init method is called
// before the service is started, and after it's determined if the program
// is running as a Windows Service.
//
// The Start method must be non-blocking.
//
// Implement this interface and pass it to the Run function to start your program.
type Service interface {
	// Init is called before the program/service is started and after it's
	// determined if the program is running as a Windows Service.
	Init(Environment) error

	// Start is called after Init. This method must be non-blocking.
	Start() error

	// Stop is called in response to os.Interrupt, os.Kill, or when a
	// Windows Service is stopped.
	Stop() error
}
```

其实跟 init.d 的脚本很像有木有。

然后我们来看下 nqsd.go 实现的这三个方法：

``` go

func (p *program) Init(env svc.Environment) error {
    // Windows 系统的服务需要适配，这里忽略
    if env.IsWindowsService() {
		dir := filepath.Dir(os.Args[0])
		return os.Chdir(dir)
	}
	return nil
}

func (p *program) Start() error {
    // 构造一个新的 Options，这个 Options 就是 nsq 自己定义的结构体，我们在后面会慢慢解析这个结构体的字段
	opts := nsqd.NewOptions()

    // 
	flagSet := nsqdFlagSet(opts)
	flagSet.Parse(os.Args[1:])

	rand.Seed(time.Now().UTC().UnixNano())

	if flagSet.Lookup("version").Value.(flag.Getter).Get().(bool) {
		fmt.Println(version.String("nsqdInstance"))
		os.Exit(0)
	}

	var cfg config
	configFile := flagSet.Lookup("config").Value.String()
	if configFile != "" {
		_, err := toml.DecodeFile(configFile, &cfg)
		if err != nil {
			log.Fatalf("ERROR: failed to load config file %s - %s", configFile, err.Error())
		}
	}
	cfg.Validate()

	options.Resolve(opts, flagSet, cfg)
	nsqdInstance := nsqd.New(opts)

	err := nsqdInstance.LoadMetadata()
	if err != nil {
		log.Fatalf("ERROR: %s", err.Error())
	}
	err = nsqdInstance.PersistMetadata()
	if err != nil {
		log.Fatalf("ERROR: failed to persist metadata - %s", err.Error())
	}
	nsqdInstance.Main()

	p.nsqdInstance = nsqdInstance
	return nil
}

func (p *program) Stop() error {
	if p.nsqdInstance != nil {
		p.nsqdInstance.Exit()
	}
	return nil
}
```

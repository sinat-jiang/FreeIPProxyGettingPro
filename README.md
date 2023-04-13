### 先简单记一下

#### ProxiesSpider
1. 最新的单 spider 结构以 zdaye 为准（04.01）；
2. 以 eightnine 和 sixsix 为例，将运行逻辑封装到 object 自身，两种写法：
    1. init 时就发送出首页请求：eightnine；
    2. init 时仅作定义，定义 run 方法封装运行逻辑：sixsix；
    
3. 小象代理失效（不提供免费代理了）
    
    
#### 项目优化
1. python 写法相关：
    1. 通用可变参数写法；
    2. 装饰器的使用；
    
2. 项目逻辑完善：
    1. spider 基类请求时添加 try catch，对异常情况调用已有代理进行请求；

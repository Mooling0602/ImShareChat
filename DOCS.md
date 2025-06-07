# ImShareChat 插件文档
这里是ImShareChat的插件文档，详细介绍配置文件作用、外部依赖和插件用法。

## 配置文件
### 主配置（config.yml）
插件的配置文件将位于`</path/to/mcdr>/config/im_share_chat/config.yml`，并包含一些简单的注释：
> 如果你从旧版本更新，默认的注释将由于配置项更新而丢失，此时你可能需要参考此处的配置文件示例。
```yml
# 接入消息互通的群聊配置
groups:
  # Matrix房间ID.
  matrix: ""
  # QQ群数字号码
  qq: ""
# 消息格式配置
format:
  # 聊天消息格式
  chat: 
    # IM平台聊天消息
    im: '[{im_platform} | {group_name}] <{user_name}> {content}'
    # Minecraft聊天消息
    game: '[MC] <{player}> {message}'
  # 玩家上线消息
  on_player_joined: '[+] {player}'
  # 玩家下线消息
  on_player_left: '[-] {player}'
  # 开服消息
  on_server_start_pre: '[MC] Server will start!'
  # 开服完成消息
  on_server_startup: '[MC] Server startup!'
  # 关服消息
  on_server_stop: '[MC] Server stopped!'
  # 崩服消息
  on_server_crash: '[MC] Server crashed!'
# 游戏事件转发配置
transfer_game_event_to_im:
  # 转发玩家死亡事件消息
  on_player_death: true
  # 转发玩家成就事件消息
  on_player_advancement: true
# 非管理员允许使用的服务器命令
allowed_rcon_commands:
  - "list"
  - "ver"
  - "version"
  - "tps"
  - "mspt"

```
其中，若启用`transfer_game_event_to_im.on_player_death`或`transfer_game_event_to_im.on_player_advancement`，你需要安装可选依赖[MoreGameEvents](https://mcdreforged.com/zh-CN/plugin/mg_events)，因为插件管理器不会在此插件的安装阶段自动下载安装此依赖。
> 此插件已适配MoreGameEvents的最新版本，你可以忽略其README中的相关警告。

### Im用户权限配置（im_permissions.yml）
v0.1.0加入了Im平台运行服务器和MCDR命令的功能，因此插件为Im用户设计了和MCDR权限类似的配置，用于管理Im用户的MCDR权限等级。

在修改并应用此配置前，你需要先详细了解[MCDR权限](https://docs.mcdreforged.com/zh-cn/latest/permission.html)是如何工作的。
```yml
owner:
admin:
helper:
user:
guest:
  - qq!12345678
  - matrix!@user:example.com

```
其中，用户的Im标识格式为`<Im平台代码>!<Im用户ID>`，各个平台的用户ID格式不一，若有疑问可打开作者的[GitHub主页](https://github.com/Mooling0602)并加入简介里的交流群进行询问，或发起Issue。

## Im平台内命令用法
### 服务器（游戏）命令
你可以遵循原版格式，发送命令内容并交由Rcon模块执行和获取返回结果，如：
```
CleMooling | 木之清泠 >>
/version
📨互通机器人🤖 >>
[ImShareChat] 命令返回结果: 
This server is running Luminol version 1.21.5-DEV-ver/1.21.5@e963af5 (2025-05-31T10:19:39Z) (Implementing API version 1.21.5-R0.1-SNAPSHOT)
You are 7 version(s) behind
Download the new version at: https://github.com/LuminolMC/Luminol
Previous version: 1.21.4-DEV-f132d2e (MC: 1.21.4)
```
目前使用的仍是MCDR的内置Rcon查询模块，如果你没有正确的配置MCDR和服务端之间的Rcon连接，功能将不可用。

### MCDR（插件）命令
你可以遵循MCDR命令的普遍格式，使用`!!`作为命令前缀，发送命令内容并交由MCDR执行和获取返回结果，如：
```
CleMooling | 木之清泠 >>
!!MCDR
📨互通机器人🤖 >>
!!MCDR: 显示这条消息
!!MCDR checkupdate: 从 Github 检测更新
!!MCDR permission: 显示权限相关的帮助信息
!!MCDR plugin: 显示插件相关的帮助信息
!!MCDR preference: 显示偏好相关的帮助信息
!!MCDR reload: 显示重载相关的帮助信息
!!MCDR server: 显示控制服务端相关的帮助信息
!!MCDR status: 显示 MCDR 状态
```

命令的权限要求等方面，请参考文档中的配置文件部分。Rcon无法获取某些命令的返回结果，具体和命令的结果输出实现方式有关。
# Windows 系统空间清理说明

这份文档专门说明：

- 什么是 `Use Disk Cleanup or DISM`
- 什么时候该用
- 应该怎么操作

适用场景：

- `cleanup-tool` 报告里看到 `C:\Windows`
- 报告提示 `Use Disk Cleanup or DISM`
- 想释放系统目录相关空间

---

## 先理解一件事

当报告里看到：

- `Windows`
- 路径：`C:\Windows`
- 处理：`Use Disk Cleanup or DISM`

它的意思不是让你**手动删除** `C:\Windows`。

它的真实意思是：

- `C:\Windows` 是系统目录
- 不能手删
- 如果要释放这部分相关空间，应该用 Windows 自带工具来“间接清理”

---

## 方法一：磁盘清理

这是最适合普通用户的方式，风险最低。

### 操作步骤

1. 按 `Win + R`
2. 输入：

```text
cleanmgr
```

3. 回车
4. 选择系统盘 `C:`
5. 点击 `清理系统文件`
6. 再次选择 `C:`
7. 勾选这些常见项：

- `Windows 更新清理`
- `临时文件`
- `传递优化文件`
- `缩略图`
- `回收站`

8. 点击确定并开始清理

### 注意

- 如果看到 `下载`，先确认里面没有重要文件
- 不确定的项目不要乱勾

---

## 方法二：DISM

这个方法主要用于清理 Windows 组件存储，适合释放系统更新和旧组件占用。

### 先打开管理员终端

可以用以下任一种方式：

1. 右键开始菜单
2. 选择：

- `Windows PowerShell(管理员)`
- 或 `终端(管理员)`

---

## 第一步：先分析组件存储

执行：

```powershell
DISM /Online /Cleanup-Image /AnalyzeComponentStore
```

这个命令不会删东西，只是分析。

你主要看它输出里关于：

- 是否推荐清理
- 组件存储大小

---

## 第二步：执行标准清理

执行：

```powershell
DISM /Online /Cleanup-Image /StartComponentCleanup
```

这个命令会清理旧组件，通常比较安全。

---

## 第三步：可选的更激进清理

如果你非常确定系统稳定，不需要回滚已安装更新，可以执行：

```powershell
DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```

### 这个命令的特点

- 会清得更彻底
- 但会让部分旧更新无法回滚

所以建议：

- 普通使用先不要跑这个
- 只有在系统已经稳定、你明确知道后果时再用

---

## 推荐顺序

推荐按这个顺序做：

1. 先跑 `cleanmgr`
2. 再跑：

```powershell
DISM /Online /Cleanup-Image /StartComponentCleanup
```

3. 如果仍想进一步清理，而且你确认系统稳定，再考虑：

```powershell
DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```

---

## 不要这样做

不要手动删除这些目录或文件：

- `C:\Windows`
- `C:\Windows\WinSxS`
- `C:\Windows\SoftwareDistribution`

除非你非常清楚自己在做什么，否则手删系统目录风险很高。

---

## cleanup-tool 里的含义

当 `cleanup-tool` 把某一项标成：

- 红灯
- `Use Disk Cleanup or DISM`

就表示：

- 这是系统级占用
- 不建议直接删
- 应该用系统工具来释放

---

## 建议

如果你只是想先安全释放一点空间：

1. 先用 `磁盘清理`
2. 再跑：

```powershell
DISM /Online /Cleanup-Image /StartComponentCleanup
```

这两个组合已经够处理大多数系统目录相关的可回收空间。

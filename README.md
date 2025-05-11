1.希望能开通抖音小店
2.希望能用抖音 发布视频


把当前文件夹的内容上传至git的步骤

1. 初始化本地 Git 仓库（如果尚未初始化）：
cd E:\nlp_pretrain_model\bb
然后，执行以下命令来初始化 Git 仓库：
git init
2. 添加文件到暂存区：
   将你想要上传的所有文件添加到 Git 的暂存区。如果你想添加所有文件，可以使用以下命令：
   git add .
3. 提交更改到本地仓库：
   提交暂存区的文件到本地仓库，并添加一个提交消息来描述你的更改：
   git commit -m "Initial commit of bb folder content"
4. 关联远程仓库：
   git remote add origin git@github.com:greatheart1000/firstgo.git
5. 创建并切换到新分支：
   创建一个新的分支，用于上传你的内容。将 <new_branch_name> 替换为你想要创建的分支名称，例如 upload-bb:
   git checkout -b <new_branch_name>
6. 推送本地分支到远程仓库：
   git push origin <new_branch_name>

完成以上步骤后，你的 E:\nlp_pretrain_model\bb 文件夹中的内容就会被上传到 GitHub 仓库 git@github.com:greatheart1000/firstgo.git 的 <new_branch_name> 分支中

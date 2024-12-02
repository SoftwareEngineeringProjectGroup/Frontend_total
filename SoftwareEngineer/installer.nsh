Section "Lambda" SecLambda
    # 输出当前工作目录和 dist_electron 目录
    DetailPrint "Current Directory: $INSTDIR"
    DetailPrint "Looking for files in dist_electron\\*"

    # 确保路径正确并复制文件
    SetOutPath $INSTDIR
    File /r "dist_electron\\*"
SectionEnd

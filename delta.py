#!/bin/bash

PNG_DIR="/path/to/hwtest"
LIBPNG_DIR="/path/to/libpng-1.6.34"

cd "$LIBPNG_DIR"

# 配置 libpng 并编译
sh ./configure CFLAGS="--coverage -static"
make clean
make

# 清理先前的覆盖率数据
rm -f *.gcda *.gcov

# 遍历 hwtest 文件夹中的每个文件
for png_file in "$PNG_DIR"/*; do
    # 检查当前文件是否在参数列表中
    if [[ " $@ " =~ " $(basename "$png_file") " ]]; then
        # 运行测试
        ./pngtest "$png_file"
    fi
done

# 收集新的覆盖率数据
gcov *.c

# 清理生成的文件
rm *.gcda pngout.png

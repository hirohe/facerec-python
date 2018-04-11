## ！该项目已停止维护！

# facerec-python

## 个人毕业设计 - 基于树莓派、OpenCV及Python语言的人脸识别

### 简介
  使用OpenCV for Python图像识别库，运行在树莓派RASPBIAN JESSIE Linux系统平台上，搭配树莓派官方摄像头模块。
  
### 运行要求
  1. OpenCV 2.4.9 for Python
  2. Python 2.7
  3. v4l2
  4. PyQt4
  
### 安装要求

  ```bash
  sudo apt-get install build-essential cmake pkg-config python-dev libgtk2.0-dev libgtk2.0 zlib1g-dev libpng-dev libjpeg-dev libtiff-dev libjasper-dev libavcodec-dev swig unzip
  ```

  1. 启用v4l2
  ```bash
  sudo nano /etc/modules
  # 增加一行记录
  bcm2835-v4l2
  # 重启后可以找到/dev/video0
  
  # 编译v4l2-util
  apt-get install autoconf gettext libtool libjpeg8 libjpeg8-dev
  git clone git://git.linuxtv.org/v4l-utils.git
  cd v4l-utils/
  sudo ./bootstrap.sh
  ./configure
  make
  sudo make install
  ```
 
  2. 编译OpenCV 2.4.9
 
  ```bash
  wget https://jaist.dl.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.9/opencv-2.4.9.zip
  unzip opencv-2.4.9.zip
  cd opencv-2.4.9/
  cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_PERF_TESTS=OFF -DBUILD_opencv_gpu=OFF -DBUILD_opencv_ocl=OFF
  
  # 要使OpenCV开启对v4l2的支持 cmake之后要有以下输出
  # V4L/V4L2:                    Using libv4l (ver 1.13.0)
  
  sudo make
  sudo make install
  ```
  
  3. 安装PyQt4
  ```bash
  sudo apt-get install python-qt4
  ```
  
  4. 运行
  ```bash
  python main.py
  ```
  
### 注意
  
  该示例运行的屏幕分辨率为竖屏480 x 800，可以修改 /boot/config.txt 的以下配置
  
  [config.txt配置说明](https://www.raspberrypi.org/documentation/configuration/config-txt.md)
  ```bash
  hdmi_cvt=800 480 60 6
  hdmi_group=2
  hdmi_mode=87
  # 设置屏幕旋转角度
  display_rotate=3
  ```

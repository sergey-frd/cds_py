#!/bin/bash

#-------------------------------------
GCC_4_8_2_PATH=/usr/local/tools/gcc/4.8.2/bin
MV7SFT_PATH=/swtools/devtools/gnueabi/arm_le/arm-none-linux-gnueabi-versions/armv7-marvell-linux-gnueabi-softfp_i686/bin
MV7SFTBE_PATH=/swtools/devtools/gnueabi/arm_be/armeb-mv7sft-linux-gnueabi/bin
MV7SFTLE_PATH=/swtools/devtools/gnueabi/arm_le/arm-mv7_sft-linux-gnueabi/bin
FREESCALE_PATH=/swtools/devtools/powerpc/freescale-2011.03/bin
ELDK_PPC_PATH=/swtools/devtools/eldk/ppc/usr/bin
ELDK_ARM_PATH=/swtools/devtools/eldk/arm/usr/bin
GNUEABI_ARM_PATH=/swtools/devtools/gnueabi/arm_le/arm-linux-gnueabi/bin
GNUEABI_ARMBE_PATH=/swtools/devtools/gnueabi/arm_be/armbe-linux-gnueabi/bin
MV5SFT_PATH=/swtools/devtools/gnueabi/arm_le/arm-mv5sft-linux-gnueabi/bin
MV5SFTBE_PATH=/swtools/devtools/gnueabi/arm_be/armbe-mv5sft-linux-gnueabi/bin

PATH=$GCC_4_8_2_PATH:$PATH:$MV7SFT_PATH:$MV7SFTBE_PATH:$MV7SFTLE_PATH:$MV5SFT_PATH:$FREESCALE_PATH:$ELDK_PPC_PATH:$ELDK_ARM_PATH:$GNUEABI_ARM_PATH:$GNUEABI_ARMBE_PATH:$MV5SFTBE_PATH
#-------------------------------------



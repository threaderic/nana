#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""

"!! The files Sconstruct.py and SconsLocalTools must be placed in the directory build/scons/
of the nana's directory !!
--> cause: relatives paths used (it could be placed in another directory
but all Paths would be modified.
"""


import os
import glob
import multiprocessing # number of processor
import pathlib # search current Directory

# Local Scons Utilities and config (see file SconsLocalTools.py)
import SconsLocalTools


# 3 build modes
vars = Variables()
vars.Add(EnumVariable('mode', 'Building mode', 'release',
                      allowed_values=('debug', 'profile', 'release')))
vars.Add(BoolVariable("progress", "Show a progress indicator during compilation", True))
vars.Add(BoolVariable("verbose", "Enable verbose output for the compilation", True))
env = Environment(variables = vars)
env.Append(CCCOMSTR = "Compiling $TARGET", LINKCOMSTR = "Linking $TARGET")

# -------------- help (type: $ scons -h)
Help(vars.GenerateHelpText(env))
#env.Decider('content')
env.Decider('MD5-timestamp')

# Compile with max processor --> for n proceesor, equivalent to: $ scons -j n
num_cpu = multiprocessing.cpu_count()
SetOption('num_jobs', num_cpu)


# -------------- Print Header information at the beginnning of the compilation
SconsLocalTools.PrintHeader(env['mode'])


if env['PLATFORM'] == 'darwin': # TODO: not tested on Windows
    env['CXX'] = 'clang++'
    env['CCFLAGS'] = '-stdlib=libc++ '
    env['LINKFLAGS'] = '-stdlib=libc++ '
elif env['PLATFORM'] == 'posix':
    env['CXX'] = 'g++'


# basic flags according to build mode
if env['mode'] == 'debug':
    env.Append(CCFLAGS = ['-g', '-fexceptions', '-Wall', '-Wextra',
                          '-Wunused-variable', '-Wfatal-errors', '-O0', '-DDEBUG'])
elif env['mode'] == 'release':
    # allow to compile in silent mode --> equivalent to: $ scons --silent
    SetOption('silent', True)

    env.Append(CCFLAGS = ['-O3', '-DNDEBUG','-w'])
    env.Append(LINKFLAGS = ['-s'])
elif env['mode'] == 'profile':
    env.Append(CCFLAGS = ['-Wall', '-pg', '-O0', '-DNDEBUG'])


# env.Append(CCFLAGS='-std=c++17 -no-pie -g3 -Wall -Wextra -I/usr/include/ -I. -I../../include/')
env.Append(CPPPATH = ['../../include/',])               # CCFLAGS = -I../../include/
env.Append(CCFLAGS='-std=c++17 -I/usr/local/include/ -I/usr/include/ -I/usr/include/freetype2')
env.Append(LIBS=['pthread','X11','Xft','fontconfig',])


##############################################################################################
##### CHECK LIBRARIES AND OTHER THINGS
##############################################################################################


env.EnsurePythonVersion(3,0)                # Python version ?
env.EnsureSConsVersion(3,0)                 # Scons version

# -------------- check for compiler and do sanity checks --------------
conf1 = Configure(env)


if not conf1.CheckCXX():
    SconsLocalTools.PrintRed('!! --> Your compiler and/or environment is not correctly configured.')
    print('!! --> You would like to build with', env['CXX'])
    Exit(0)
else:
    SconsLocalTools.PrintGreen('(i) Your Library / Program will be built with: ' + env['CXX'] + ' ')

if not conf1.CheckLib('png'):
    print('PNG Library not found')
    Exit(1)

# keep any changes you may have performed
env = conf1.Finish()

# -------------- check for Librairies dependecies --------------
# function SconsLocalTools.CheckPKGConfig / CheckPKG define in SconsLocalTools.py
conf2 = Configure(env, custom_tests = { 'CheckPKGConfig' : SconsLocalTools.CheckPKGConfig,
                                       'CheckPKG' : SconsLocalTools.CheckPKG
                                       })

lib_x11 = 'x11 >= 1.0.0'
if not conf2.CheckPKG(lib_x11):
    SconsLocalTools.PrintRed('please install the package libx11-dev ' +
                         lib_x11 +
                         '// X11 client-side library (development headers) ')
    Exit(1)

lib_xcursor = 'xcursor >= 1.0.0'
if not conf2.CheckPKG(lib_xcursor):
    SconsLocalTools.PrintRed('please install the package libxcursor-dev ' +
                         lib_xcursor +
                         '// X cursor management library (development files)')
    Exit(1)

lib_xft = 'xft >= 2.0.0'
if not conf2.CheckPKG(lib_xft):
    SconsLocalTools.PrintRed('please install the package libxft-dev ' +
                             lib_xft +
                             '// FreeType-based font drawing library for X (development files)')
    Exit(1)

lib_pkg_conf = '0.15.0'
if not conf2.CheckPKGConfig(lib_pkg_conf):
    SconsLocalTools.PrintRed('please install the package pkg-config ' +
                             lib_pkg_conf +
                             '// manage compile and link flags for libraries')
    Exit(1)

lib_alsa = 'alsa >= 1.0.0'
if not conf2.CheckPKG(lib_alsa):
    SconsLocalTools.PrintRed('please install the package libasound2-dev ' +
                        lib_alsa +
                        '// Advanced Linux Sound Architecture (ALSA) - Library')
    Exit(1)

env = conf2.Finish()


##############################################################################################
##### BUILD AND LINK
##############################################################################################


# search all cpp files in the source directory
# matches_cpp_files = ['../../source/unicode_bidi.cpp',
#                      '../../source/any.cpp','../../source/basic_types.cpp']
matches_cpp_files = glob.glob('../../source/**/*.cpp', recursive = True)

obj = env.Object(source = matches_cpp_files)
# print(obj,len(obj))
# for i in obj:
# print("The object file is: %s" %obj[i])


# -------------- generate the library --------------
# lib = env.Library('Library/nana', source = obj)
# --> library/libnana.a (relative to the Sconstruct file)
lib = env.Library('library/nana', source = obj)


print("The object file is: %s" %lib[0])


# -------------- copy also the library to the directory /build/bin
# (relative to the Sconstruct file)
path_to_bin = pathlib.Path.cwd().parent / 'bin'
lib_copy = env.Install(path_to_bin, lib)
aa = env.AlwaysBuild(lib_copy)

## using Alias could be another solution
# env.Default(lib_copy)
## --> type: $ scons install
# env.Alias('install', '/usr/bin')

# --> if the library won't be erased with call: $ scons -c
# env.NoClean(lib_copy)
import SCons.Node.FS
#somelist = SCons.Node.get_contents_dir(lib)


# print('aa', SCons.Node.FS.(aa).exists())
aa = env.GetBuildPath(lib)
# print(aa,len(aa))

# bb = env.Dictionary()
# print(bb,len(bb))
# print("${TARGET}")



# finish command priting foot message
finish_command = env.Command('finish', [], action=SconsLocalTools.print_finish, num_cpu=num_cpu, envMode=env['mode'])

env.Depends( finish_command, lib_copy )
if 'finish' not in lib_copy:
    lib_copy.append('finish')

# The following only makes sense when the 'env' is defined, and assumes it is.
if "env" in locals():
    # 100, number of nodes calculated at end of compilation in debug mode and copied here
    SconsLocalTools.show_progress(env, 100, env['mode'], "Library Nana")

import sys
import os
import multiprocessing # number of processor

# color 
os.system("") # activation of this function https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
screen = sys.stdout
    

#x = 0
#for i in range(50):
 #colors = ""
 #for j in range(5):
   #code = str(x+j)
   #colors = colors + "\33[" + code + "m\\33[" + code + "m\033[0m "
 #print(colors)
 #x=x+5

# Terminal, color, return carriage, cls
def clearTerminal(): 
    os.system('cls||clear')
    
def PrintReturn():
    screen.write('\n')

def PrintRed(text, width = 80, sep = ' '):
    screen.write('\033[31m' + text.ljust(width,sep) + '\033[0m\n')
 
def PrintRedFilled(text, width = 80, sep = ' '):
    screen.write('\033[41m' + text.ljust(width,sep) + '\033[0m\n')
   
def PrintBlue(text, width = 80, sep = ' '):
    screen.write('\033[34m' + text.ljust(width,sep) + '\033[0m\n')
    
def PrintBlueFilled(text, width = 80, sep = ' '):
    screen.write('\033[44m' + text.ljust(width,sep) + '\033[0m\n')

def PrintGreen(text, width = 80, sep = ' '):
    screen.write('\033[32m' + text.ljust(width,sep) + '\033[0m\n')
    
def PrintGreenFilled(text, width = 80, sep = ' '):
    screen.write('\033[42m' + text.ljust(width,sep) + '\033[0m\n')
    



def PrintHeader(envMode = 'release'):
    num_cpu = multiprocessing.cpu_count()
    clearTerminal()
    PrintReturn()
    
    # basic flags according to build mode
    if envMode == 'debug' or envMode == 'profile':
        PrintRedFilled('',sep = '-')
        PrintRedFilled('#     running with %s processors' % num_cpu)
        PrintRedFilled('#     compiling in debug|profile mode')
        PrintRedFilled('#     --> $ scons -j %s mode=%s' % (num_cpu, envMode))
        PrintRedFilled('#     if other mode wanted, please type: $ scons -h')
        PrintRedFilled('#     For help on scons, please type: $ scons -H')
        PrintRedFilled('',sep = '-')
    elif envMode == 'release':
        PrintBlueFilled('',sep = '-')
        PrintBlueFilled('#     running with %s processors' % num_cpu)
        PrintBlueFilled('#     compiling in release mode, silent')
        PrintBlueFilled('#     --> $ scons -j %s mode=%s --silent'.ljust(60,' ') % (num_cpu, envMode))
        PrintBlueFilled('#     if other mode wanted, please type: $ scons -h')
        PrintBlueFilled('#     For help on scons, please type: $ scons -H')
        PrintBlueFilled('',sep = '-')




def finish(  num_cpu,envMode ):
    print('\nDO IT \n\n')
    
    # basic flags according to build mode
    if envMode == 'debug' or envMode == 'profile':
        PrintRedFilled('',sep = '-')
        PrintRedFilled('#     running with %s processors' % num_cpu)
        PrintRedFilled('#     compiling in debug|profile mode')
        PrintRedFilled('#     --> $ scons -j %s mode=%s' % (num_cpu, envMode))
        PrintRedFilled('#     if other mode wanted, please type: $ scons -h')
        PrintRedFilled('#     For help on scons, please type: $ scons -H')
        PrintRedFilled('',sep = '-')
    elif envMode == 'release':
        PrintBlueFilled('',sep = '-')
        PrintBlueFilled('#     running with %s processors' % num_cpu)
        PrintBlueFilled('#     compiling in release mode, silent')
        PrintBlueFilled('#     --> $ scons -j %s mode=%s --silent'.ljust(60,' ') % (num_cpu, envMode))
        PrintBlueFilled('#     if other mode wanted, please type: $ scons -h')
        PrintBlueFilled('#     For help on scons, please type: $ scons -H')
        PrintBlueFilled('',sep = '-')

    # raise Exception( 'DO IT' )





def show_progress(env, number_of_nodes = 316, mode = 'release', nameTarget = 'Library'):

    from SCons.Script import Progress, Command, AlwaysBuild

    node_count_data = {
        "count": 0,
        "max": number_of_nodes,
        "interval": 1,
        "fname": str(env.Dir("#")) + "/.scons_node_count",
    }


    class cache_progress:
        def __init__(self, path=None):
            self.path = path            

        def __call__(self, node, *args, **kw):
            if show_progress:
                # Print the progress percentage
                node_count_data["count"] += node_count_data["interval"]
                node_count = node_count_data["count"]
                node_count_max = node_count_data["max"]
                if node_count_max > 0 and node_count < node_count_max and mode == 'release':
                    screen.write('\033[34m' + ("\r[%3d%%] %s" % ((node_count * 100 / node_count_max), int(node_count * 100 / node_count_max / 2) * '#'))  )
                    screen.write(("%s \r" % (int((node_count_max - node_count) * 100 / node_count_max / 2) * '_')) + '\033[0m' )
                    screen.flush()
                elif node_count_max > 0 and node_count < node_count_max and (mode == 'debug' or mode == 'profile'):
                    screen.write('\033[31m' + "\r[%3d%%] %s" % ((node_count * 100 / node_count_max), int(node_count * 100 / node_count_max / 2) * '#'))
                    screen.write(("%s \n" % (int((node_count_max - node_count) * 100 / node_count_max / 2) * '_')) + '\033[0m' )
                    screen.flush()
                elif node_count_max > 0 and node_count > node_count_max*2:
                    screen.write("\r[100%] ")
                    screen.flush()
                elif node_count >= node_count_max and mode == 'release':
                    PrintReturn()
                    PrintBlue('\n[100%] ' + 'build of %s finished ;) !' % (nameTarget))
                    PrintBlue("#      to suppress builded files, type $ scons -c")
                    PrintReturn
                    screen.flush()
                    progress_finish_command = Command("progress_finish", [], progress_finish)
                elif node_count >= node_count_max and (mode == 'debug' or mode == 'profile'):
                    PrintReturn()
                    PrintRed("['[100%] ' + 'build of %s finished ;) !' % (nameTarget)")
                    PrintReturn()
                    PrintRed('#     --> number of nodes: ')
                    PrintRed('#     %s'% node_count)
                    PrintRed('#     --> put to the function SconsTools.show_progress() in the Soncscript file: ')
                    PrintRed("#     to suppress builded files, type $ scons mode=(debug) (profile) -c")
                    PrintReturn()
                    screen.flush()
                    progress_finish_command = Command("progress_finish", [], progress_finish)
                else:
                    screen.write("\n\n[Initial build] ")
                    screen.flush()


    def progress_finish(target, source, env):
        with open(node_count_data["fname"], "w") as f:
           f.write("%d\n" % node_count_data["count"])


    try:
        with open(node_count_data["fname"]) as f:
            node_count_data["max"] = int(f.readline())
    except:
        pass

    Progress(cache_progress(), interval=node_count_data["interval"])
    
##############################################################################################################################
###  FUNCTIONS CLASS FOR CONFIGURATION, CHECKLIBRARIES

def CheckPKGConfig(context, version):
     context.Message( 'Checking for pkg-config... ' )
     ret = context.TryAction('pkg-config --atleast-pkgconfig-version=%s' % version)[0]
     context.Result( ret )
     return ret

def CheckPKG(context, name):
     context.Message( 'Checking for %s... ' % name )
     ret = context.TryAction('pkg-config --exists \'%s\'' % name)[0]
     context.Result( ret )
     return ret

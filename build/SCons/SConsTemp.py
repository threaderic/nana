import pathlib
import os

p = pathlib.Path.cwd().parent / 'bin'

print(p)




####################################################
# Progressbar example

env.Replace(  CCCOMSTR        = "Compiling  [$SOURCE]",
              CXXCOMSTR       = "Compiling  [$SOURCE]",
              FORTRANPPCOMSTR = "Compiling  [$SOURCE]",
              FORTRANCOMSTR   = "Compiling  [$SOURCE]",
              SHCCCOMSTR      = "Compiling  [$SOURCE]",
              SHCXXCOMSTR     = "Compiling  [$SOURCE]",
              LINKCOMSTR      = "Linking    [$TARGET]",
              SHLINKCOMSTR    = "Linking    [$TARGET]",
              INSTALLSTR      = "Installing [$TARGET]",
              ARCOMSTR        = "Archiving  [$TARGET]",
              RANLIBCOMSTR    = "Ranlib     [$TARGET]")

screen = open('/dev/tty', 'w')
node_count = 0
node_count_max = 0
node_count_interval = 1
node_count_fname = str(env.Dir('#')) + '/.scons_node_count'

def progress_function(node):
    global node_count, node_count_max, node_count_interval, node_count_fname
    node_count += node_count_interval
    if node_count > node_count_max: node_count_max = 0
    if node_count_max>0 :
        screen.write('\r[%3d%%] ' % (node_count*100/node_count_max))
        screen.flush()

def progress_finish(target, source, env):
    global node_count
    with open(node_count_fname, 'w') as f: f.write('%d\n' % node_count)

try:
    with open(node_count_fname) as f: node_count_max = int(f.readline())
except: pass
Progress(progress_function, interval=node_count_interval)

progress_finish_command = Command('progress_finish', [], progress_finish)
Depends(progress_finish_command, BUILD_TARGETS)
if 'progress_finish' not in BUILD_TARGETS:     
    BUILD_TARGETS.append('progress_finish')
    
    
    
    
#[  0%] Installing [/Users/davidl/HallD/builds/sim-recon/Darwin_macosx10.11-x86_64-llvm8.0.0/bin/MakeEventWriterROOT.pl] 
#[  0%] Installing [/Users/davidl/HallD/builds/sim-recon/Darwin_macosx10.11-x86_64-llvm8.0.0/bin/MakeReactionPlugin.pl] 
#[  0%] Compiling  [programs/Simulation/genr8/genkin.c] 
#[  0%] Compiling  [programs/Simulation/genr8/genr8.c] 
#[  3%] Compiling  [programs/Utilities/hddm/hddm-cpp.cpp] 
#[  3%] Compiling  [programs/Utilities/hddm/XString.cpp] 
#[  3%] Compiling  [programs/Utilities/hddm/XParsers.cpp] 
#[  3%] Compiling  [programs/Utilities/hddm/md5.c] 
#[  4%] Compiling  [external/xstream/src/base64.cpp] 
#[  4%] Compiling  [external/xstream/src/bz.cpp] 
#[  4%] Compiling  [external/xstream/src/common.cpp] 
#[  4%] Compiling  [external/xstream/src/dater.cpp] 
#[  4%] Linking    [.Darwin_macosx10.11-x86_64-llvm8.0.0/programs/Simulation/genr8/genr8] 
#[  4%] Installing [/Users/davidl/HallD/builds/sim-recon/Darwin_macosx10.11-x86_64-llvm8.0.0/bin/genr8] 
#[  4%] Compiling  [external/xstream/src/debug.cpp] 
#[  4%] Compiling  [external/xstream/src/digest.cpp]
 #...

########################################################

#This creates a command that depends on the default targets for it's execution (so you know it'll always run last - see DEFAULT_TARGETS in scons manual). Hope this helps.

#Nice solution, but it only works when you are building a Default Target. I exchanged your last 2 lines for this: Depends(finish_command, BUILD_TARGETS); if 'finish' not in BUILD_TARGETS: BUILD_TARGETS.append('finish') – Omar Kohl Jun 13 '14 at 13:39


def finish( target, source, env ):
    raise Exception( 'DO IT' )

finish_command = Command( 'finish', [], finish )
Depends( finish_command, DEFAULT_TARGETS )
Default( finish_command )


########################################################


from pympler.classtracker import ClassTracker

class MemStats(Stats):
    def __init__(self):
        Stats.__init__(self)
        classes = [SCons.Node.Node, SCons.Node.FS.Base, SCons.Node.FS.File,
                   SCons.Node.FS.Dir, SCons.Executor.Executor]
        self.tracker = ClassTracker()
        for c in classes:
            self.tracker.track_class(c)
    def do_append(self, label):
        self.tracker.create_snapshot(label)
    def do_print(self):
        stats = self.tracker.stats
        stats.print_summary()
        stats.dump_stats('pympler.stats')
        
        
###############################################################


# Call function inside SCons Builder's action


cmdVars = Variables(None, ARGUMENTS)
cmdVars.AddVariables(
    EnumVariable('DEBUG', 'help for debug', 'a', allowed_values=('a','b','c')),
    PathVariable('CLI', 'path to cli exe', 'C:\...\blah.exe', PathVariable.PathIsFile)
)

env = Environment(variables = cmdVars)

def generateSomeExtraBitsDependingOnFlag(source, target, env, for_signature):
    if (env['DEBUG'] == 'a'):
         print("aaaaa"
         return "-DDEBUG -DBlah myTextHere"
    return ''


env['generateSomeExtraBitsDependingOnFlag'] =generateSomeExtraBitsDependingOnFlag

myBuilder = env.Builder(
    action = '"$CLI" ${generateSomeExtraBitsDependingOnFlag}'
)

env.Append(BUILDERS = {'myBuilder' : myBuilder})

env.myBuilder('dummy','input')

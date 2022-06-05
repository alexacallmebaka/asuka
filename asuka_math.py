import nextcord
from nextcord.ext import commands
import neon_genesis_integration as ngi

#Math commands live here.
class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    commands.group(name="Math commands")

    @commands.command(name='dot')
    async def dot(self, ctx, *args):
        """Will return the dot product of two vectors. \n Input vectors in the form <a,b,c> where a, b, and c are real numbers."""
        
        #a and b are vectors. They are derved from input in the form of <,a,b,c>. 
        #From each element, we strip off the angle brackets, and then create a list by splitting at commas.
        #Finally, we run through the list turning each string value to an int, and then take the object spit out by map() and make a tuple.
        a = tuple(map(int,args[0][1:-1].split(',')))
        b = tuple(map(int,args[1][1:-1].split(',')))
       
        #Check to see if vectors are the same length.
        if len(a) == len(b):

            #Initialize result integer
            result = 0

            #Sum up the products of the components of both vectors.
            for i in range(len(a)):
                result += a[i]*b[i]
        await ctx.reply(result)

    @commands.command(name='cross')
    async def cross(self, ctx, *args):
        """Will return the cross product of two three-dimensional vectors.\n Input vectors in the form <a,b,c> where a, b, and c are real numbers."""
        
        #These vectors are constructed the same way they are in the dot product command. See the comment there.
        a = tuple(map(int,args[0][1:-1].split(',')))
        b = tuple(map(int,args[1][1:-1].split(',')))

        #Make sure both vectors are in three dimensions.
        if len(a) == len(b) == 3:

            #Plug the vectors into the formula for the determinant of a 3x3 matrix.
            await ctx.reply("`<{},{},{}>`".format(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]))
    
    @commands.command(name="pi")
    async def pi(self,ctx):
        """Easy access to π."""
        await ctx.send("π")

    @commands.command(name="int")
    async def integrate(self, ctx, *args):
        """Does numeric integration. Input as you would a TI-89 calculator.\n
        Takes the following arguments, in order: function,variable of integration,bottom bound,top bound\n
        Has support of most common special functions (ln, trig, etc.). When using pi, please use π.\n
        Example input: &int sin(x+3)e^(x-4)+9,x,1,7"""
        
        #Mush all the elements into one string, expunge the whitespace, and then seperate based on commas.
        #Should result in [function, variable, lower bound, upper bound].
        args = ' '.join(args).replace(' ','').split(',')

        try:
            sum = ngi.integrate(args[0], args[1], float(args[2]), float(args[3]))
            await ctx.reply(sum)
        except OverflowError:
            await ctx.reply("That number is too big! Overflow error!")
        except ZeroDivisionError:
            await ctx.reply("This integral does not converge (zero division error).")
        except:
            await ctx.reply("An unknown error has occured. Please make sure your input is syntacticly correct, and makes sense.")

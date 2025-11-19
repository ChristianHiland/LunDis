from discord.ext import commands
import discord
import json


class Progress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Scene Learning.
        self.scene_progress_data = {0: {"Scenes": 4, "Learned": 3}}
        self.scene_save = "Data/SceneProgress.json"

        # Tasks
        self.todos_data = {0: [{"Todo Name": "Bot", "Todo": "Make Bot", "Status": False}]}
        self.todos_save = "Data/TodoProgress.json"

        # Load Data
        self.GetData()

    async def GetData(self):
        # Update Scene Data
        with open(self.scene_save, "r") as file:
            self.scene_progress_data = json.load(file)
        # Update Todo Data
        with open(self.todos_save, "r") as file:
            self.todos_data = json.load(file)

    async def UpdateSavedData(self):
        with open(self.scene_save, "w") as file:
            json.dump(self.scene_progress_data, file, indent=4)
        with open(self.todos_save, "w") as file:
            json.dump(self.todos_data, file, indent=4)
    
    # Update / Make Scene Progress
    @commands.command(name="sceneUpdate")
    async def sceneUpdate(self, ctx, learnedScenes: int, maxScenes: int):
        "Update or Make a Scene Progress Track"
        # Get Member & and ID
        user_id = ctx.author.id
        
        # Temp Data
        temp = {"Scenes": maxScenes, "Learned": learnedScenes}
        self.scene_progress_data[user_id] = temp
        await ctx.send(f"Updated {ctx.author.display_name}'s Scene Progress. Keep Going! Pls We only have a week left...")
        self.UpdateSavedData()

    # Get Member's Progress
    @commands.command(name="sceneProgress")
    async def sceneProgress(self, ctx, member: discord.Member = None):
        """Get Current Scene Progress"""
        if member is None:
            member = ctx.author
        # Get ID
        user_id = member.id
        try:
            await ctx.send(f"{member.display_name} has {self.scene_progress_data[user_id]["Learned"]}/{self.scene_progress_data[user_id]["Scenes"]} learned.")
        except:
            await ctx.send("Please make a progress check, using >sceneUpdate before running is command.")

    # Add Member's Todo.
    @commands.command(name="addTodo")
    async def addTodo(self, ctx, todo_name: str, todo: str):
        """Add a Todo to your todo list."""
        member = ctx.author
        user_id = member.id
        temp = {"Task Name": todo_name, "Task": todo}
        try:
            print(self.todos_data[user_id])
        except:
            self.todos_data[user_id] = []
            self.todos_data[user_id].append(temp)
        await ctx.send(f"Updated {member.display_name} Todos! Total Things To Do: {len(self.todos_data[user_id])}. Keep Going!")
        self.UpdateSavedData()

    # Get a Member's Todos.
    @commands.command(name="seeTodos")
    async def seeTodos(self, ctx, member: discord.Member = None):
        """See your todos, or another member."""
        if member == None:
            member = ctx.author
        user_id = member.id
        await ctx.send(f"{member.display_name}'s Todo")
        for todo in self.todos_data[user_id]:
            await ctx.send(f" - {todo["Task"]} (With Name: {todo["Task Name"]})\n")

async def setup(bot):
    await bot.add_cog(Progress(bot))
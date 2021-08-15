const Discord = require("discord.js");
const cmd = require("node-cmd");
const fs = require("fs");


const client = new Discord.Client();

client.on("ready", () => {
    console.log("Wassup g!");
});

client.on("message", msg => {
    if (!msg.author.bot) {

        if (msg.content === "!namaz") {
            // Run the python file
            cmd.runSync('python main.py');
            // Read the json
            const data = fs.readFileSync('namaz.json', 'utf-8')
            // Parse the json
            const jsonData = JSON.parse(data);
            
            msg.channel.send(`The next namaz is ${jsonData.closest_prayer.namazName}, I will notify you when its time!`)
            

            setTimeout(function () {
                msg.reply("Its " + jsonData.closest_prayer.namazName + " time!")
            }, jsonData.closest_prayer.microsecondsLeft);
        }

        if (msg.content === "ping!") {
            msg.reply("pong!");
        }
    }
});

token = fs.readFileSync("token.txt", "utf-8");

client.login(token);
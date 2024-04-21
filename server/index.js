const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const config = require("./config");
const chatManager = require("./chatManager");
const clientManager = require("./clientManager");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static("../client"));

io.on("connection", (socket) => {
  console.log("A user connected");
  clientManager.addClient(socket);

  // User Connect
  // User Disconnect
  // User Change Name
  // User Join Group
  // User Create Group
  // User leave Group
  // User Message

  socket.on("disconnect", () => {
    console.log("User disconnected");
    clientManager.removeClient(socket);
  });

  socket.on("message", (msg) => {
    chatManager.handleMessage(socket, msg);
  });

  socket.on("createGroup", (groupName) => {
    chatManager.createGroup(socket, groupName);
  });
});

server.listen(config.port, () => {
  console.log(`Server running on port ${config.port}`);
});

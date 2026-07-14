# Ideabot

Discord bot for saving ideas

## Features
* Save and retrieve ideas via slash commands
* Or, save an idea by replying to a message and tagging the ideabot
* All ideas are saved with references to the user, server, and channel. They can only be retrieved by the same user on the same server and channel.

## Usage

### Slash Commands:

#### `/idea`

Store your idea. The user, channel, and server are automatically picked up from context. Replies with a thumbs-up emoji

Replies with a Thumbs-up emoji if successful. If there's an error, it will reply with a thumbs-down emoji and a message.

**Arguments:**

| Argument    | Type | Required | Description                                                       |
|-------------|------|----------|-------------------------------------------------------------------|
| idea        | str  | yes      | The description of your idea                                      |
| name        | str  | no       | An optional name to give to your idea                             |
| category    | str  | no       | An optional category to assign to your idea                       |
| shared_with | str  | no       | Add the idea to another user's ideas list in addition to your own |

#### `/remember`

Fetch your stored ideas. Will only return ideas stored by you in the same channel and server.

Replies with all filtered ideas.

**Arguments:**

| Argument | Type | Required | Description                   |
|----------|------|----------|-------------------------------|
| name     | str  | no       | Name of idea to filter on     |
| category | str  | no       | Category of idea to filter on |


#### `/dump`

Dump all your ideas as a JSON file.

**Arguments:**

| Argument     | Type | Required | Description                                   |
|--------------|------|----------|-----------------------------------------------|
| idea_name    | str  | no       | Name of idea to filter on                     |
| category     | str  | no       | Category of idea to filter on                 |
| all_channels | bool | no       | Return ideas from all channels. Default False |
| all_servers  | bool | no       | Return ideas from all servers. Default False  |

#### `/search name`

Search ideas by idea name. The bot will give you a dropdown so you can select the idea name(s).


#### `/search categories`

Search ideas by idea category. The bot will give you a dropdown so you can select the idea category/categories.

### Mentions

You won't always have the idea. Or you might but you don't want to (or forget) to use the slash command. Fortunately, there's another option.

Fortunately, you can still save that idea by tagging @ideabot in a reply to the message. You may optionally also add a category and name by separating them by commas.

Examples:

```
@anotheruser: Let's take over the world
↳ @you: @ideabot
```

Result: Ideabot remembers that you saved the idea "Let's take over the world".

```
@anotheruser: Let's take over the world
↳ @you: @ideabot domination
```

Result: Ideabot remembers that you saved the idea "Let's take over the world" with the category "domination".

```
@anotheruser: Let's take over the world
↳ @you: @ideabot domination, World Control
```

Result: Ideabot remembers that you saved the idea "Let's take over the world" with the category "domination" and name "World Control".

```
@anotheruser: Let's take over the world
↳ @you: @ideabot domination, World Control @thirduser @fourthuser
```

Result: Ideabot remembers that you saved the idea "Let's take over the world" with the category "domination" and name "World Control". It also saves it for @thirduser and @fourthuser.

## API

Ideabot comes with a built-in API which binds to `0.0.0.0:12345`. All endpoints require a key. All `/admin` endpoints require a key belonging to an admin.

If the database does not yet exist, a key will be generated for you and displayed in the logs.

### Authenticating

Authentication is passed via the `Authorization` header with the value `Bearer <KEY>`.  User is determined from the key.

### Endpoints:

#### `/ideas/get`

**Description:** Retrieve your ideas.

**Parameters:**

| Name         | Type             | Required | Description           |
|--------------|------------------|----------|-----------------------|
| idea_name    | str \| list[str] | no       | Name(s) to search     |
| category     | str \| list[str] | no       | Category(s) to search |
| server_name  | str \| list[str] | no       | Server(s) to search   |
| channel_name | str \| list[str] | no       | Channel(s) to search  |


**Successful response schema:**

```json
[
  {
    "server": "string",
    "channel": "string",
    "idea": "string",
    "user": "string",
    "category": "string",
    "idea_name": "string"
  }
]
```

#### `/ideas/create`

**Description:** Create a new idea.

**Parameters:**

| Name         | Type | Required | Description                       |
|--------------|------|----------|-----------------------------------|
| idea         | str  | yes      | Idea you are adding               |
| idea_name    | str  | no       | Name to give the idea             |
| category     | str  | no       | Category for the idea             |
| server_name  | str  | no       | Discord server to store the idea  |
| channel_name | str  | no       | Discord channel to store the idea |

**Successful response:** No response.


#### `/admin/add_user`

**Description:** Create a new API user.

Note: Creating an API user is NOT required to use the bot. Anyone on the server can still interact with it and their ideas will be stored under their user name. However, they will be unable to retrieve their ideas unless an account is created using their global Discord username.

**Parameters:**

| Name         | Type | Required | Description                   |
|--------------|------|----------|-------------------------------|
| user_name    | str  | yes      | Name of user to create        |
| admin        | bool | no       | Whether user has admin powers |

**Successful response:** String containing API key. Key can never be recovered after this.


## Creating and using the bot

1. Navigate to the [Discord Developer's Portal](https://discord.com/developers/applications). Create a new application and name it "ideabot" (or any other name you would prefer).
2. In the Discord Developer's Portal page for your bot, navigate to "Installation". Set the install link to "None" and save.
3. Navigate to the "Bot" tab. Enable "Message Content Intent" and save.
4. Still in the "Bot" tab, copy the token listed under "Token". If it is not visible, click "Reset Token" and follow the prompt. Save this and never share it - this is the private Discord token that we will need to set up the container.
5. Use the [docker-compose.yml](./docker-compose.yml) file to help you set up your container. The environment variable `DISCORD_TOKEN` will be the token from the previous step. Go ahead and spin this up.
6. Back in the Discord Developer's Portal, navigate to the "OAuth2" tab:
  a. In the "OAuth2 URL Generator" section, select the scopes "bot" and "applications.commands"
  b. In the "Bot Permissions" section, select "Manage Messages", "Read Message History", and "Use Slash Commands".
7. Navigate to the URL generated at the bottom and grant your bot permission on the proper server.

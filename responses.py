async def responses(message):
    if message.content.startswith('cookie'):
        await message.channel.send("🍪")

    if message.content.startswith('free'):
        await message.channel.send('<https://youtu.be/xvFZjo5PgG0>')

    if message.content.startswith('coc'):
        await message.channel.send('🐔')

    if message.content.startswith('77+33'):
        await message.channel.send('100')

    if message.content.startswith('33+77'):
        await message.channel.send('100')

    if message.content.startswith('goofy'):
        await message.channel.send('ahh')

    if 'kiss' in message.content:
        print(f'react to {message.author}')
        await message.add_reaction("😽")

    if 'dick' in message.content:
        print(f'react to {message.author}')
        await message.add_reaction("🍆")

    if 'onix' in message.content:
        print(f'react to {message.author}')
        await message.add_reaction("🤡")

# for amaze
# moving all the responses to their own file makes it easier to manage
# if you dont like it, you can revert EVERYTHING with this command:
# git revert --no-commit d646d34bc0a232581dc0126163c7a5aa84ec0a01..HEAD
# you can view how it originally looked and then commit it

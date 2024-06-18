server:

- npm run build (compilen typescript)
- npx prisma migrate om database migratie te starter
- kopieren dist folder
- kopieren .js files uit src folder
- server starten met npm run start met NODE_ENV=production ervoor.

NODE_ENV=production

client:

- npm run build.
- client/dist map deployen

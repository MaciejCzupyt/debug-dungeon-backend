# Debug Dungeon

The backend of a project for listing, creating and commenting on educational programming mini-projects.

[//]: # (## Lint)

[//]: # (## Build)

[//]: # (## Deploy)

[//]: # (## License)

# TODO

Project management:

Implementation:

- [x] Create new models
- [x] Create serializers with rest-framework
- [x] Create views
- [x] Plug views to URLs
- [ ] Add screenshots from the index view and projects details view in readme
- [x] Create a view for user management - creating accounts, without the ability to list other users
- [x] Fix ability to create user without password
- [x] Update serializers/models to include the owner username in the JSON instead of user id
- [ ] Make sure that only the owner can delete their resources (probably add validation in a view)
- [x] Set timestamp to "now" on save always
- [x] Update resource owners on save too
- [x] Fix POST username/password, password isn't being hashed

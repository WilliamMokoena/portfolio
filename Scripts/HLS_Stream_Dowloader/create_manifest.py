# If manifest.m3u8 was manually downloaded but contains urls.
# The following code will parse it so only the file names are added to the local manifest.

with open('./playlist.m3u8', 'r') as f:
    file = f.readlines()

manifest = []
for el in file:
    el = el[:-1]
    if 'https' in el:
        el = el.split('/')
        el = el[len(el)-1]
        manifest.append(el)

    else:
        manifest.append(el)

with open('./manifest.m3u8', 'a') as f:
    for elm in manifest:
        f.write(elm+'\n')

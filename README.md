# MagazineRack
A Python app to browse a collection of PDFs (scanned magazines in my case).

You point the **Magazine Rack** at a directory that contains your magazine (PDF) content (in the file: `magazine_rack.py`, the line: `app = MagazineRack('content')` — replace `'content'` with the relative path to the base directory of your magazines). **Magazine Rack** provides an onscreen directory navigation UI (with limitations on depth and breadth — see below). Directories are navigable entirely with key presses. Files are indicated with a magazine icon and decoration to indicate approximate percentage of the magazine that has been viewed.

<p align="center">
<img width="1000" src="https://github.com/EngineersNeedArt/MagazineRack/blob/f49e7ee2b63ab3dd5173abad2f45c7f59e63abc4/screenshots/BrowserUI.jpg">
  <br>
<em>The navigation UI.</em>
</p>

When a magazine (PDF) is selected, hitting the ENTER key dismisses the navigation UI and displays the pages of the magazine "two-up". Key presses allow navigation through the magazine from start to end. Progress through each magazine is stored for display in the navigation UI as mentioned previously.

<p align="center">
<img width="1000" src="https://github.com/EngineersNeedArt/MagazineRack/blob/f49e7ee2b63ab3dd5173abad2f45c7f59e63abc4/screenshots/TwoUp.jpg">
  <br>
<em>Reading a magazine (two-up).</em>
</p>

I have found various archives of vintage magazines scanned to PDF but prefer to download them for offline reading. Traveling in an RV for example, you can't always expect internet accessibility. Additionally though I wanted a dedicated reader app that was otherwise distraction-free. And one that also recorded which magazines were read/completed.

I enjoy, for example, perusing old hobbyist electronics magazines looking at the various projects. As there were quite a number of these magazines, knowing which ones I had already scanned was important.

Although intended for (and tested on) a Raspberry Pi, most of the development has been on MacOS where it also works well.

### State

Version 1.0 is just complete. This version is useable for paging through PDF's. A directory of your PDF collection can be displayed and navigated in order to load a new PDF. There are limitations however (see below).

### Directory Structure

The root of yur PDF directory is specified near the bottom of the `magazine_rack.py` file. By default it is `'content'`. This path specified is relative to where the project is located. In the default case you will create a directory called `content` alongside the `magazine_rack.py` file. In here you will put your PDFs. The structure of your PDF directory must follow specific guidelines as I will describe.

The PDF (directory) browser in the **Magazine Rack** app displays vertical columns of file listings — the left-most column represents the contents of the base directory you specified above. A user can select a file listed in a column and if it is a directory they have selected, the column to the right will display the contents of that directory.

### Limit Number of Items in a Directory to 26

The contents of the directory, as displayed in the column, do not scroll. Therefore, how many items are allowed in a directory or sub-directory is dictated by how many files can be displayed vertically in the app. Too many items and some will be clipped and not visible to the user. For the font chosen in the app and a debug screen size of 768 vertical pixels, the limit on the number of items that are displayed turns out to be 26. You can decrease the font size in the directory browser in the app or you can run the app on a larger screen size (make sure `DEBUG = False`) to get more than 26 items per directory, but I think that going any higher makes it slower for the user to navigate up and down.

If you have a PDF collection, let's say old *Popular Mechanics* magazine issues as scanned PDFs. If you have only 20 or so, just put them in a folder called `Popular Mechanics` directly within your `contents` directory. If you have more than 26, then perhaps group them into sub-directories by year. For most magazines of course (including `Popular Mechanics`), there will only be 12 issues per year and so each year directory will be well under the 26 file limit.

If you have a *very* large collection that covers more than 26 years you can create sub-sub-directories where you group the years by decade. As an example, you might have a path to one of your `Popular Mechanics` issues that looks like `contents/Popular Mechanics/1960's/1964/Popular Mechanics 1964-05.pdf`. So at the top level is the `Popular Mechanics` directory containing all the decades you have including `1960's`. Within `1960's` you may directories for each of the ten years of that decade including `1964`. And with `1964` you have the 12 issues from that year (including May's issue `Popular Mechanics 1964-05`).

### Limit Depth of Directory Structure to 4

And the above example leads to the other significant limitation of the directory structure. There are only ever four columns displayed in the **Magazine Rack** directory browser UI, so your PDF collection cannot be more than 4 levels deep. To go back to the previous example I gave an example path to a specific *Popular Mechanics* issue as something like `contents/Popular Mechanics/1960's/1964/Popular Mechanics 1964-05.pdf`. We don't count the base directory (`contents`) but there are nonetheless 4 additional components in that path: 1: `Popular Mechanics`, 2: `1960's`, 3: `1964`, and `Popular Mechanics 1964-05.pdf`. That is the limit of what we can display within the UI.

You should not find this last limitation too bad even for a rich PDF collection (like the example for *Popular Mechanics*) so long as it begins at the root of the base directory.

The above limitations can be resolved in the future by additional code to allow for scrolling — both vertically and horizontally. I am loathe to tackle the limitation at this point in part because I think that an overly nested, overly long directory of magazines makes casual browsing more tedious. I also have not yet run hit up against these limitations yet with my own PDF collection.

### Other Considerations

The width of the columns, like the height, is limited by the screen size (its width divided by 4). And like the limit on the number of rows, how long the name of a file can be displayed is a factor of this width and the font chosen. I intentionally use a narrow font to allow for longer file names. I also strip the suffix (`.pdf`) from the file names.

If any string in the directory path to the file is "prefixed" in the file name, this is removed from the file name as well. In the previous example the target file name was `Popular Mechanics 1964-05.pdf`. As stated above, `.pdf` is removed so it is shortened and displayed as `Popular Mechanics 1964-05`. Additionally, since `Popular Mechanics` is part of the path, the file name displayed is further reduced to just `1964-05`.

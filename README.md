# Description

This program runs through Super Mario Maker 2 courses and identifies them for you if they contain a specified object (power-up, enemy, block, etc.).

# Setup

Ideally you have `pyenv` or some equivalent python version manager installed. This section will assume `pyenv`.

1. Install the local python version from `.python-version` and packages in `requirements.txt`. If you're using `pyenv` you can use the following make command

```
make install
```

2. You need something to decrypt the encrypted SMM2 course. The  files are encrypted for transfer over the wire so this is a required step. My personal go to has been to compile [JiXiaomi's SMM2-Decryptor](https://github.com/JiXiaomai/SMM2-Decryptor). This is going to pair most simply with this program. Ensure the compiled decryptor is named `courseDecryptor` and is located at this program's root.

It's worth mentioning alternatives since they're all good and my choice was ill informed at the time of writing this code.

- There's also [simontime's SMM2CourseDecryptor](https://github.com/simontime/SMM2CourseDecryptor). This also requires compilation. 
- If you would prefer an uncompiled solution instead [jonbarrow's patrick](https://github.com/jonbarrow/partrick) has a file called [encryption.js](https://github.com/jonbarrow/partrick/blob/7c8589503ae017bd71c3d018e6ca2f5b249d67a0/src/encryption.js#L10C10-L10C21) with the necessary functionality.

These may require small refactors to this project to ensure the interfaces line up. Again, JiXiaomi's decryptor is assumed to be the default for this project.


With that, you should be ready to go.

# Usage

## Running

Usage is as simple as:

```
make collect-courses
```

This will begin running the script for a maximum of 12 hours or until you SIGINT the script. The script commits its transactions per course it identifies so you can `ctrl+c` out at any time.

Searching courses by difficulty or setting alternative maximum durations are also supported. For more information use `python main.py --help`.

## Retrieving Results

To retrieve courses simple use:

```
make get-course
```

This retrieves a random course from the DB. Other retrieval args are supported such as course difficulty filtering and returning several courses. You can use `python main_db.py --help` for information on supported options.

## Searching for specific objects

### IDs

This program supports searching for courses with specific objects in them in SMM2. A reference for what we're about to talk about can be found here: https://github.com/liamadvance/smm2-documentation/blob/master/Object%20Information.md

Objects are identified by an ID in the course files. This ID can be supplied when calling `main.py` via the `--wanted_id` option. The following command would save courses that contain the Fire Flower powerup (because that's the object with ID 34 on the linked SMM2 object documentation).

```
python main.py --wanted-id 34
```

### Flags

If you've played SMM2 you'll know that there are some power-ups that you can only place by placing a power-up and then holding select on it and turning it into the desired power-up from the pop-up menu. Some objects in this category include:
- Master Sword
- Superball Flower
- SMB2 Mushroom

These Objects have the same ID as the one you initially have to place which makes finding them challenging.

There's woefully little documentation on this at the previously mentioned source but this script still supports it because I enjoy playing courses with these powerups. If you do to, here's how you'd use the script:

```
python main.py ---wanted-id 34 --wanted_flag 00000110000000000000000000000100
```

This command would search courses for the Object with ID 34 (Fire Flower) for the flag represented by the bit-string above. That bit string is actually the one that identifies the Superball Flower. All courses returned by that invocation of `main.py` would contain at least 1 Superball Flower. 
If you want to find a specific power up that requires a flag: feel free to leave an issue on this repository and we can figure out what the flag is.
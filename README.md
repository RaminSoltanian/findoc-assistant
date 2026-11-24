# Pre-work tool

`prework.py` sets up your Johto pre-work task in a Docker container (the
"lane"). You run Claude Code in the lane with your own Claude login. Then the
tool collects the diff and the transcript for your Studio task.

## Before you start

You need:

- macOS, Linux, or Windows with WSL. Native Windows is not supported. On
  Windows, open a WSL terminal and work in a folder in your WSL home.
- Python 3.9 or newer (`python3 --version`).
- Git.
- Docker Desktop, OrbStack, colima, or Docker Engine. Start it before setup.
- About 3 GB of free disk: the lane image download (0.7 GB), the image once
  loaded into Docker, and the repository.

## 1. Download and verify the files

1. Open the Setup page on the dashboard: https://cc-johto.vercel.app/setup
2. Make a new, empty folder for your task.
3. Download into it (the page's "Download all" buttons do this in one click):
   - `prework.py`, this `README.md`, and `Dockerfile.lane` (reference only:
     how the lane image was built);
   - the lane image for your computer (about 0.7 GB): `arm64` for an Apple
     Silicon Mac, `amd64` for an Intel Mac or an Intel/AMD Windows or Linux PC.
     If your browser saves it to your Downloads folder, you can leave it there
     (on WSL, setup also looks in your Windows Downloads folder).
4. Check the tool files against the Setup page. In the task folder, paste the
   `shasum -a 256 -c` command from the page; every line must say `OK`. Do not
   run the file if one does not. You don't need to check the image by hand:
   setup checks it before loading it.

## 2. Set up the lane

In the task folder, run:

```sh
python3 prework.py setup
```

Setup asks for two values from your Studio task:

- **Task**: the task name, for example `Task l50u5a0c`.
- **Repo URL**: for example `https://github.com/<owner>/<repo>` or
  `https://github.com/<owner>/<repo>/tree/<commit>`.

You can also give them as flags:

```sh
python3 prework.py setup --task "Task l50u5a0c" --repo https://github.com/<owner>/<repo>
```

If the Repo URL has no commit, setup uses the latest commit on the default
branch and prints it. Use `--commit <40-character sha>` to start from a
different commit.

The first setup on a computer checks the image you downloaded and loads it into
Docker, which takes a minute or two. Later setups on the same computer skip it.

Use a new, empty folder for each run, including another run of the same
task. To run two lanes at once, set up the second lane in its own folder. The
first lane can keep running. Each lane gets its own ports. The lanes use
separate CPUs when Docker has enough of them. Two lanes need Docker with 8 GB
of memory or more.

## 3. Do the run

```sh
cd model_a
./claude-dev
```

1. On the first launch, type `/login`. Sign in with your own Claude account.
   The login stays in this task's lane. Your own Claude Code is not changed.
2. Paste your opening prompt and do the run.
3. Finish with `/exit`.

If you close the window or press Ctrl+Z, run `./claude-dev` again. It goes back
to the same session.

Dev servers in the lane use ports 3000-3019 and 8000-8009. They open on your
computer at one of these pairs of ports:

- 34000-34019 and 35000-35009.
- 36000-36019 and 37000-37009.

Setup prints the pair that your lane uses.

## 4. Collect the outputs

Go back to the task folder and run:

```sh
cd ..
python3 prework.py collect
```

Collect writes these files to `prework_output/`:

| File | Studio field |
| --- | --- |
| `final.diff` | Final Output |
| the session `.jsonl` transcript | Conversation Log |

Attach both files to your task in Studio. Collect never copies your Claude
login.

Collect prints the files to attach only when it wrote a new diff and found a
transcript. Otherwise it says what failed and ends with an error. Fix the
problem, then run collect again. A diff from an earlier collect is then
renamed to `final.previous-<time>.diff`. It may miss later work. An empty
`final.diff` is correct when the run changed no code.

## Troubleshooting

- **Docker is not answering.** Start Docker, wait until it is running, then run
  the command again. Your lane and your work are not lost.
- **The lane's ports are taken.** Setup prints a `docker stop` command for
  each pre-work lane that is running. Another program can also hold the ports.
  Then setup prints a port to look up with `lsof -i`. Stop one lane or that
  program, then run setup again. A stopped lane keeps its work. Its
  `./claude-dev` starts it again when its ports are free.
- **Docker has less than 8 GB of memory.** Then only one lane can run at a
  time. Stop the other lane first, or give Docker more memory in its settings.
- **Another run.** Use a new, empty folder for each run.

## What the tool creates

- In the task folder: `model_a/claude-dev`, `prework-manifest.json`,
  `prework_output/`, and `.prework-*` files.
- In your home folder: `~/.mercor-prework/`. It holds each lane's Claude
  config and login.
- In Docker: the image `mercor-prework-lane`, and containers, volumes and
  networks named `prework-*`.

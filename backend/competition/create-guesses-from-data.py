#! /usr/bin/env python3

from pathlib import Path
import json
import hashlib

def main():
    directory = Path(__file__).parent / 'data'
    target_directory = Path(__file__).parent / 'guesses'
    target_directory.mkdir(exist_ok=True)
    for jsonfile in sorted(directory.glob('*'), key=lambda x: x.name[-15:]):
        try:
            content = json.loads(jsonfile.read_text())
            email_address = content['emailAddress']
            twitch_username = content['twitchUsername']
            guess = content['guess']
            guess_serialised = json.dumps(guess)
            if email_address != '':
                email_hash = hashlib.sha256(email_address.lower().encode('utf-8')).hexdigest()
                email_path = target_directory / f'{email_hash}.json'
                email_path.write_text(guess_serialised)
            if twitch_username != '':
                twitch_hash = hashlib.sha256(twitch_username.lower().encode('utf-8')).hexdigest()
                twitch_path = target_directory / f'{twitch_hash}.json'
                twitch_path.write_text(guess_serialised)
        except:
            print(f'skipping {jsonfile}')


if __name__ == '__main__':
    main()

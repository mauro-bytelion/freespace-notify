import re
import argparse
import requests
import subprocess


def send_message(integration, server, channel, subject, message):
    hook = 'https://hooks.slack.com/services/{}'.format(integration)
    subject = '{} | {}'.format(subject, server)
    data = {
        'text': message,
        'channel': channel,
        'username': subject,
    }
    requests.post(hook, json=data)


def strip_NaN(string):
    return int(re.sub(r"[^\d+]","", string))


def format_message(server, line):
    free_pc = 100 - int(strip_NaN(line.get('Use%')))
    return (
        "RUNNING OUT OF SPACE!",
        "Server {} has only {} of free space ({}% of {} Total)".format(
            server, line.get('Avail'), free_pc, line.get('Size')
        )
    )


def df_h():
    dfdata = []
    df = subprocess.check_output(["df -h"],
                                 universal_newlines=True,
                                 shell=True)

    output = df.replace("Mounted on", "Mounted_on")
    data = [re.sub(" +", ",", line).split(",")
            for line in output.split("\n")]

    for line in data[1:]:
        line_dct = {}
        for col in range(len(line)):
            line_dct.update({data[0][col]: line[col]})
        dfdata.append(line_dct)

    return dfdata


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token',
                        type=str,
                        help="Slack Integration Token")
    parser.add_argument('-c', '--channel',
                        type=str,
                        default="#test",
                        help="Slack channel to send the report")
    parser.add_argument('-s', '--server',
                        type=str,
                        help="Server Name")
    parser.add_argument('-m', '--mounted-on',
                        type=str,
                        help="'Mounted on' value")
    parser.add_argument('-u', '--used',
                        type=int,
                        default=75,
                        help="Send alert if Used % is greater than ...")
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help="Use only if DEBUG")

    args = parser.parse_args()
    if args.mounted_on and args.used and args.server:
        df = df_h()
        for line in df:
            if line.get('Mounted_on') == args.mounted_on \
               and strip_NaN(line.get('Use%')) >= args.used:
                subject, message = format_message(args.server, line)
                if not args.debug and args.token:
                    send_message(
                        args.token,
                        args.server,
                        args.channel, subject, message)
                else:
                    print(
                        args.server,
                        args.channel, subject, message
                    )

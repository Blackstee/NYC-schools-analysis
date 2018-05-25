
import program_for_quest as program_for_quest
import program_hosts as program_hosts
import data.mongo_setup as mongo_setup
import parser
import downloader as down
import generator
import services.data_service as svc
import analysis as an
from schools.parser import get_data, get_data_distr


def main():
    mongo_setup.global_init()

    print_header()

    #down.downloader()
    #get_data()
    #get_data_distr()

    #generator.make_schools_full()

    #svc.generate_scores_all()

    #program_hosts.rate_class()
    #program_hosts.update_average_scores_everywhere()

    #an.analysis_students()
    #an.analysis_districts()

    #svc.add_districts_all()
    try:
        while True:
            if find_user_intent() == 'client':
                program_for_quest.run()
            else:
                program_hosts.run()
    except KeyboardInterrupt:
        return


def print_header():
    snake = \
        """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄░░░░░░░░░
░░░░░░░░█░░░░░░░░░░░░▄█▄▄░░▄░░░█░▄▄▄░░░
░▄▄▄▄▄░░█░░░░░░▀░░░░▀█░░▀▄░░░░░█▀▀░██░░
░██▄▀██▄█░░░▄░░░░░░░██░░░░▀▀▀▀▀░░░░██░░
░░▀██▄▀██░░░░░░░░▀░██▀░░░░░░░░░░░░░▀██░
░░░░▀████░▀░░░░▄░░░██░░░▄█░░░░▄░▄█░░██░
░░░░░░░▀█░░░░▄░░░░░██░░░░▄░░░▄░░▄░░░██░
░░░░░░░▄█▄░░░░░░░░░░░▀▄░░▀▀▀▀▀▀▀▀░░▄▀░░
░░░░░░█▀▀█████████▀▀▀▀████████████▀░░░░
░░░░░░████▀░░███▀░░░░░░▀███░░▀██▀░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 """
    print(snake)
    print("Welcome to NYC school statistic!")
    print("Why are you here?")

    print()


def find_user_intent():
    print("[g] Get the rating of NYC schools")
    print("[h] Make analysis")
    print()
    choice = input("Are you a [g]uest or [h]ost? ")
    if choice == 'h':
        return 'admin'

    return 'client'


if __name__ == '__main__':
    main()

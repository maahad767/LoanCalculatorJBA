import math
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type")
    parser.add_argument("--principal", type=int)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--payment", type=int)
    parser.add_argument("--interest", type=float)

    args = parser.parse_args()

    if len(sys.argv) != 5:
        print('Incorrect parameters')
        quit(1)

    if args.type != 'diff' and args.type != 'annuity':
        print(args.type != 'diff')
        print('Incorrect parameters')
        quit(2)

    if args.type == 'diff' and args.payment is not None:
        print('Incorrect parameters')
        quit(3)

    if args.interest is None or args.interest < 0:
        print('Incorrect parameters')
        quit(4)
    interest = args.interest / 100 / 12
    if args.type == 'diff' and args.principal is not None and args.principal > 0 \
            and args.periods is not None and args.periods > 0:
        calculate_differentiated_payment(principal=args.principal, periods=args.periods, interest=interest)
    elif args.type == 'annuity':
        if args.principal is None and args.payment is not None and args.payment > 0 \
                and args.periods is not None and args.periods > 0:
            calculate_principal(annuity_payment=args.payment, periods=args.periods,
                                interest=interest)  # calculate principal
        elif args.payment is None and args.principal is not None and args.principal > 0 \
                and args.periods is not None and args.periods > 0:
            calculate_annuity_payment(principal=args.principal, periods=args.periods,
                                      interest=interest)  # calculate payment
        elif args.periods is None and args.principal is not None and args.principal > 0 \
                and args.payment is not None and args.payment > 0:
            calculate_periods(principal=args.principal, monthly_payment=args.payment,
                              interest=interest)  # calculate period
    else:
        quit(5)


def calculate_periods(principal, monthly_payment, interest):
    periods = math.ceil(math.log(monthly_payment / (monthly_payment - interest * principal), 1 + interest))

    years = periods // 12
    months = periods % 12

    if years and months:
        print(f'It will take {years} {"years" if years > 1 else "year"} '
              f'and {months} {"months" if months > 1 else "month"} to repay this loan!')
    elif years:
        print(f'It will take {years} {"years" if years > 1 else "year"} to repay this loan!')
    elif months:
        print(f'It will take {months} {"months" if months > 1 else "month"} to repay this loan!')

    over_payment = monthly_payment * periods - principal
    print(f'Overpayment = {over_payment}')


def calculate_annuity_payment(principal, periods, interest):
    annuity_payment = math.ceil(principal * ((interest * math.pow(1 + interest, periods))
                                             / (math.pow(1 + interest, periods) - 1)))

    print(f'Your monthly payment = {annuity_payment}!')
    over_payment = annuity_payment * periods - principal
    print(f'Overpayment = {over_payment}')


def calculate_principal(annuity_payment, periods, interest):
    principal = math.floor(annuity_payment / (interest * math.pow(1 + interest, periods) /
                                              (math.pow(1 + interest, periods) - 1)))

    print(f'Your loan principal = {principal}!')

    over_payment = annuity_payment * periods - principal
    print(f'Overpayment = {over_payment}')


def calculate_differentiated_payment(principal, periods, interest):
    total = 0
    for month in range(1, periods + 1):
        diff = math.ceil((principal / periods) + (interest * (principal - (principal * (month - 1)) / periods)))
        total += diff
        print(f'Month {month}: payment is {diff}')

    over_payment = total - principal
    print(f'\nOverpayment = {over_payment}')


if __name__ == '__main__':
    main()

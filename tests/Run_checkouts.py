# Run checkout flows


def run_tests(login, password):

    auth_status = input("Type 'login' for tests with logged in user or 'anon' for tests "
                        "with anonymous user.\nIf you want to run all tests, type 'all' "
                        "(no quotes).\n")
    if auth_status == 'login':
        print('\nRunning checkouts for logged in user...\n')
        from tests.FFp1vol import init_checkout       # check Freemium (input: any pdf up to 160, pp or cc)
        init_checkout(login, password)
        from tests.FFp1vol import init_checkout       # check Freemium plus (free - input: 160 portrait pages pdf, pp or cc)
        init_checkout(login, password)
        from tests.FFp1vol import init_checkout       # check Freemium plus (Credit Card - input: 25 pdf, cc)
        init_checkout(login, password)
        from tests.FFp1vol import init_checkout       # check Freemium plus (PayPal - input: 25 pdf, pp)
        init_checkout(login, password)
        from tests.FFp2vol import init_checkout       # check two Freemium plus (free - select 160 portrait pages pdf)
        init_checkout(login, password)
        from tests.FFp2vol import init_checkout       # check two Freemium plus (Credit Card - select 25 portrait pages pdf)
        init_checkout(login, password)
        from tests.FFp2vol import init_checkout       # check two Freemium plus (Paypal - select 25 portrait pages pdf)
        init_checkout(login, password)
        from tests.S1vol import init_checkout         # check Standard
        init_checkout(login, password)
        print('\nFinished tests for logged in user.')
    elif auth_status == 'anon':
        print('\nRunning checkouts for anonymous user...\n')
        print('\nFinished tests for anonymous user.')
    elif auth_status == 'all':
        print('\nRunning checkouts for both logged in and anonymous user...\n')
        # logged in flows:
        from tests.FFp1vol import init_checkout  # check Freemium (input: any pdf up to 160, pp or cc)
        init_checkout(login, password)
        from tests.FFp1vol import init_checkout  # check Freemium plus (free - input: 160 portrait pages pdf, pp or cc)
        init_checkout(login, password)
        from tests.FFp1vol import init_checkout  # check Freemium plus (Credit Card - input: 25 pdf, cc)
        init_checkout(login, password)
        from tests.FFp1vol import init_checkout  # check Freemium plus (PayPal - input: 25 pdf, pp)
        init_checkout(login, password)
        from tests.FFp2vol import init_checkout  # check two Freemium plus (free - select 160 portrait pages pdf)
        init_checkout(login, password)
        from tests.FFp2vol import init_checkout  # check two Freemium plus (Credit Card - select 25 portrait pages pdf)
        init_checkout(login, password)
        from tests.FFp2vol import init_checkout  # check two Freemium plus (Paypal - select 25 portrait pages pdf)
        init_checkout(login, password)
        from tests.S1vol import init_checkout  # check Standard
        init_checkout(login, password)

        # anonymous flows:
        print('\nFinished tests for all users.')
    else:
        print('\nSomething went wrong. Probably, there was a typo in your input.\n')
    input('\nTests are successfully finished! Press Enter to exit.')


if __name__ == "__main__":
    login = input('Login: ')
    password = input('Password: ')
    run_tests(login, password)

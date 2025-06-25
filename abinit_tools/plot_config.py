def setup(use_pgf=True):

    import matplotlib

    if use_pgf:
        matplotlib.use('pgf')

    import matplotlib.pyplot as plt

    if use_pgf:
        plt.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': True,
        })

    return plt




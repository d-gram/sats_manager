from setuptools import setup

APP = ['front/new_ui.py']
DATA_FILES = [
    ('resources', [
        'resources/appicon.icns',
        'resources/bitcoin-btc-logo.png',
        'resources/bitcoin-seeklogo.svg'
    ]),
    ('fonts', [
        'resources/fonts/MiriamLibre-Bold.ttf',
        'resources/fonts/MiriamLibre-Regular.ttf'
    ])
]
OPTIONS = {
    'argv_emulation': False,
    'packages': ['requests',
                 'matplotlib',
                 'customtkinter',
                 'bitcoinlib',
                 'bip_utils',
                 'PIL',
                 'cairosvg'],
    'plist': {
        'CFBundleName': 'SATS_MANAGER',
        'CFBundleDisplayName': 'SATs Manager',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0'
    },
    'iconfile': 'resources/appicon.icns'
}

setup(
    app=APP,
    name='SATS Manager',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)

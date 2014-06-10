from distutils.core import setup

setup(
    name="leave-tracker",
    version="1.0",
    packages=['leave_tracker',
              'leave_tracker/management',
              'leave_tracker/management/commands',
              'leave_tracker/templatetags'
              ],
    package_dir={'leave_tracker': 'leave_tracker'},
    package_data={'leave_tracker': ['templates/*.html',
                               'templates/leave_tracker/*.html',
                               'templates/leave_tracker/*.txt',
                               ]
    },
    author="Agiliq Solutions",
    author_email="hello@agiliq.com",
    description="A django based leave tracker",
    long_description=
    """
Leave tracking system. All users can request leaves. Admins can grant leaves.
""",)
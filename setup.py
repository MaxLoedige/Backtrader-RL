from setuptools import setup, find_packages

setup(
   name='backtrader_rl',
   version='0.2',
   description='Reinforcement Environment for Finacial trading based on the Backtrader infrastructure',
   author='Max Lödige',
   # author_email='foomail@foo.com',
   packages = ["backtrader_rl","backtrader_rl.adapters"],  # would be the same as name
   install_requires=['backtrader', 'gym', 'tensorforce', 'ray[rllib]'], #external packages acting as dependencies
)

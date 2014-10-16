# django-stashboard

The original Stashboard was developed by Twilio to provide status information on our phone, SMS, and Communication APIs. They open sourced it to provide a generic status page designed to be customized by any hosted services company to provide customers up-to-date status information.

The original is dependent on Google App Engine, this fork removes the dependency and makes this a pure-Django project, using the traditional ORM.

## Installation

To add Stashboard to an existing Django application, first of install "django-stashboard" - the code is available on pypi.

	pip install django-stashboard

Next, you should add `stashboard` to your `INSTALLED_APPS` in the project settings module.

	INSTALLED_APPS = (
		...
		'stashboard',
		'rest_framework',  # API
		...
	)

## Demo

The most recent version of Stashboard lives at http://stashboard.appspot.com

## Documentation

Full documentation can be found on [Read The Docs](http://readthedocs.org/docs/stashboard/en/latest)

## Community

All Stashboard development and discussion happens in the [Stashboard google group](https://groups.google.com/forum/#!forum/stashboard)

To keep up to date, you can follow [@stashboard](http://twitter.com/stashboard) on Twitter or join the [#stashboard](irc://irc.freenode.net/stashboard) channel on freenode

## Development

You'll need to install a couple more packages to hack on Stashboard
  
    pip install -r requirements.txt

To run the unit tests, 

    python tests/runner.py tests

## Future

The [roadmap](https://github.com/twilio/stashboard/wiki/Roadmap) details future plans for Stashboard.

## Acknowledgements
* Buttons by [Necolas](https://github.com/necolas/css3-github-buttons)
* Fugue icons by [Yusuke Kamiyamane](http://p.yusukekamiyamane.com/)
* Iconic icons by [P.J. Onori](http://somerandomdude.com/projects/iconic/)
* OAuth support via [simplegeo/python-oauth2](https://github.com/simplegeo/python-oauth2)

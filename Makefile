clean: 
	rm -rf dist

dist: 
	python setup.py bdist_wheel
	echo "Output can be found here: `find dist -name '*.whl'`"

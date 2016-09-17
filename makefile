.DEFAULT_GOAL := test

FILES :=                              \
    Netflix.html                      \
    Netflix.log                       \
    Netflix.py                        \
    RunNetflix.in                     \
    RunNetflix.out                    \
    RunNetflix.py                     \
    TestNetflix.out                   \
    TestNetflix.py

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint3.5
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.4
    AUTOPEP8 := autopep8
endif

.pylintrc:
	$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@

Netflix-tests:
	git clone https://github.com/cs373g-fall-2016/Netflix-tests.git

Netflix.html: Netflix.py
	pydoc3 -w Netflix

Netflix.log:
	git log > Netflix.log

RunNetflix.tmp: Netflix.py RunNetflix.in RunNetflix.out RunNetflix.py .pylintrc
	-$(PYLINT) Netflix.py
	-$(PYLINT) RunNetflix.py
	$(PYTHON) ./RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	diff RunNetflix.tmp RunNetflix.out

TestNetflix.tmp: Netflix.py TestNetflix.py .pylintrc
	-$(PYLINT) TestNetflix.py
	$(COVERAGE) run    --branch TestNetflix.py >  TestNetflix.tmp 2>&1
	$(COVERAGE) report -m                      >> TestNetflix.tmp
	cat TestNetflix.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  Netflix.html
	rm -f  Netflix.log
	rm -f  RunNetflix.tmp
	rm -f  TestNetflix.tmp
	rm -rf __pycache__

config:
	git config -l

format:
	$(AUTOPEP8) -i Netflix.py
	$(AUTOPEP8) -i RunNetflix.py
	$(AUTOPEP8) -i TestNetflix.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: Netflix.html Netflix.log RunNetflix.tmp TestNetflix.tmp Netflix-tests check

versions:
	which make
	make --version
	@echo
	which git
	git --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	which $(PYDOC)
	$(PYDOC) --version
	@echo
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	$(PIP) list


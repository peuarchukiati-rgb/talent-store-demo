# talent-store-demo test lab. Offline needs no key, no CLI and no network.
.PHONY: lab lab-1 lab-2 lab-3 lab-4 lab-5 lab-real lab-real-1 lab-real-3 verify test

lab:            ## run all 5 suites offline (order 1 2 5 3 4)
	./lab/run.sh --mode offline
lab-1:
	./lab/run.sh --suite 1 --mode offline
lab-2:
	./lab/run.sh --suite 2 --mode offline
lab-3:
	./lab/run.sh --suite 3 --mode offline
lab-4:
	./lab/run.sh --suite 4 --mode offline
lab-5:
	./lab/run.sh --suite 5 --mode offline

lab-real:       ## run all suites in real mode (codex_cli + claude_cli, no API key)
	./lab/run.sh --mode real
lab-real-1:
	./lab/run.sh --suite 1 --mode real
lab-real-3:
	./lab/run.sh --suite 3 --mode real

verify:         ## check the committed raw layer against the manifest
	python3 cli.py verify
test:           ## run the engine quote-check unit test
	python3 tests/test_quote_check.py

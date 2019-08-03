travis:
	@-iverilog -V
	@cd test && ./lint.sh
	@cd test && ./regression.sh

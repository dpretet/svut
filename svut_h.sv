// Copyright 2019 The SVUT Authors
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
// associated documentation files (the "Software"), to deal in the Software without restriction,
// including without limitation the rights to use, copy, modify, merge, publish, distribute,
// sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
// is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all copies or substantial
// portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
// NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
// WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
// SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


`ifndef INFO
`define INFO(msg) \
        $display("\033[0;37mINFO:     [%g] %s\033[0m", $time, msg)
`endif

`ifndef SUCCESS
`define SUCCESS(msg) \
        $display("\033[0;32mSUCCESS:  [%g] %s\033[0m", $time, msg)
`endif

`ifndef WARNING
`define WARNING(msg) \
        $display("\033[1;33mWARNING:  [%g] %s\033[0m", $time, msg); \
        svut_warning += 1
`endif

`ifndef CRITICAL
`define CRITICAL(msg) \
        $display("\033[1;35mCRITICAL: [%g] %s\033[0m", $time, msg); \
        svut_critical += 1
`endif

`ifndef ERROR
`define ERROR(msg, msg2="", prefix="ERROR:   ") \
        $display("\033[1;31m%s [%g] %s %s\033[0m", prefix, $time, msg, msg2); \
        svut_error += 1
`endif

`ifndef SVUT_SETUP
`define SVUT_SETUP \
    integer svut_status = 0; \
    integer svut_warning = 0; \
    integer svut_critical = 0; \
    integer svut_error = 0; \
    integer svut_error_total = 0; \
    integer svut_nb_test = 0; \
    integer svut_nb_test_success = 0; \
    string svut_test_name = ""; \
    string svut_suite_name = "";
`endif

`ifndef LAST_STATUS
`define LAST_STATUS svut_status
`endif

`ifndef FAIL_IF
`define FAIL_IF(exp) \
    if (exp) begin \
        `ERROR("FAIL_IF"); \
        svut_status = 1; \
    end else begin \
        svut_status = 0; \
    end
`endif

`ifndef FAIL_IF_NOT
`define FAIL_IF_NOT(exp, reason="", assertion="FAIL_IF_NOT") \
    if (!exp) begin \
        `ERROR(assertion, reason); \
        svut_status = 1; \
    end else begin \
        svut_status = 0; \
    end
`endif

`ifndef ASSERT
`define ASSERT(exp, reason="") \
    `FAIL_IF_NOT(exp, reason, "ASSERT ");
`endif

`ifndef FAIL_IF_EQUAL
`define FAIL_IF_EQUAL(a,b) \
    if (a === b) begin \
        `ERROR("FAIL_IF_EQUAL"); \
        svut_status = 1; \
    end else begin \
        svut_status = 0; \
    end
`endif

`ifndef FAIL_IF_NOT_EQUAL
`define FAIL_IF_NOT_EQUAL(a,b, reason="", assertion="FAIL_IF_NOT_EQUAL") \
    if (a !== b) begin \
        `ERROR(assertion, reason); \
        svut_status = 1; \
    end else begin \
        svut_status = 0; \
    end
`endif

`ifndef ASSERT_EQUAL
`define ASSERT_EQUAL(a,b, reason="") \
    `FAIL_IF_NOT_EQUAL(a, b, reason, "ASSERT_EQUAL ");
`endif

`ifndef ASSERT_EQUALS
`define ASSERT_EQUALS(a,b, reason="") \
    `ASSERT_EQUAL(a,b, reason)
`endif

/* Test and Test suite definition  ********************************************
 * "Fail if" style
 *  `UNIT_TESTS -- Call to define an unnamed test suite
 *  `UNIT_TESTS_END -- End unnamed test suite
 *
 *  `TEST_SUITE(name) -- Define a named test suite (name is shown in test output)
 *  `TEST_SUITE_END -- End a named test suite (name is shown in test output)
 *
 *  `UNIT_TEST(label) -- begin a unit test and give it a label
*   `UNIT_TEST_END -- end a unit test
*/

`ifndef NAMED_TEST
`define NAMED_TEST(name="test") \
    begin \
        $display("\033[0;34mTESTING:  [%g] %s\033[0m", $time, name); \
        setup(); \
        svut_test_name = name; \
        svut_error = 0; \
        svut_nb_test = svut_nb_test + 1;
`endif

`ifndef NAMED_TEST_END
`define NAMED_TEST_END \
        #0; \
        teardown(); \
        if (svut_error == 0) begin \
            svut_nb_test_success = svut_nb_test_success + 1; \
            `SUCCESS("Test successful\n"); \
        end else begin \
            `ERROR("Test failed ", svut_test_name); \
            $display(""); \
            svut_error_total += svut_error; \
        end \
    end
`endif

`ifndef UNIT_TEST
`define UNIT_TEST(label) \
    `NAMED_TEST()
`endif

`ifndef UNIT_TEST_END
`define UNIT_TEST_END \
    `NAMED_TEST_END
`endif

`ifndef TEST_SUITE
`define TEST_SUITE(name, prefix="TEST_SUITE: ") \
    task run(); \
    begin \
        svut_suite_name = name; \
        $display("\n\033[0;36m%s %s execution started\033[0m\n", prefix, name);
`endif

`ifndef TEST_SUITE_END
`define TEST_SUITE_END \
    end \
    endtask \
    initial begin\
        run(); \
        $display("\n\033[0;36mTEST SUITE:  %s execution finished @ %g\033[0m\n", svut_suite_name, $time); \
        if (svut_warning > 0) begin \
            $display("\t  -> \033[1;33mWarning number: %4d\033[0m", svut_warning); \
        end \
        if (svut_critical > 0) begin \
            $display("\t  -> \033[1;35mCritical number: %4d\033[0m", svut_critical); \
        end \
        if (svut_error_total > 0) begin \
            $display("\t  -> \033[1;31mError number: %4d\033[0m", svut_error_total); \
        end \
        if (svut_nb_test_success != svut_nb_test) begin \
            $display("\t  -> \033[1;31mSTATUS: %4d / %4d test(s) passed\033[0m\n", svut_nb_test_success, svut_nb_test); \
        end else begin \
            $display("\t  -> \033[0;32mSTATUS: %4d / %4d test(s) passed\033[0m\n", svut_nb_test_success, svut_nb_test); \
        end \
        $finish(); \
    end
`endif

`ifndef UNIT_TESTS
`define UNIT_TESTS \
    `TEST_SUITE("Testsuite", "INFO:    ");
`endif

`ifndef UNIT_TESTS_END
`define UNIT_TESTS_END \
    `TEST_SUITE_END
`endif


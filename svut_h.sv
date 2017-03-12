// Copyright 2017 Damien Pretet ThotIP
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


`ifndef UNIT_TESTS
`define UNIT_TESTS \
    reg test_error = 0;\
    reg error = 0;\
`endif

`ifndef UNIT_TEST
`define UNIT_TEST \
    error = 0;\
`endif

`ifndef UNIT_TEST_END
`define UNIT_TEST_END \
    if (error > 0)
        `ERROR("Error(s) happened during test run")
`endif

`ifndef UNIT_TESTS_END
`define UNIT_TESTS_END \
    if (test_error > 0)\
        `ERROR("Test(s) failed during testsuite run")\
`endif

`ifndef FAIL_IF
`define FAIL_IF(a) \
    if (a)\
        error = 1\
`endif

`ifndef FAIL_IF_EQUAL
`define FAIL_IF_EQUAL(a,b) \
    if (a === b)\
        error = 1\
`endif

`ifndef FAIL_IF_NOT_EQUAL
`define FAIL_IF_NOT_EQUAL(a,b) \
    if (a !== b)\
        error = 1\
`endif

`ifndef INFO
`define INFO(msg)
    $display("INFO:    [%0t][%0s]: %s", $time, name, msg)
`endif

`ifndef WARNING
`define WARNING(msg)
    $display("WARNING: [%0t][%0s]: %s", $time, name, msg)
`endif

`ifndef ERROR
`define ERROR(msg)
    $display("ERROR:   [%0t][%0s]: %s", $time, name, msg)
`endif


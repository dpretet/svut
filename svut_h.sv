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


`ifndef INFO
`define INFO(msg) \
    $display("INFO:    [%0t]: %s", $time, msg);
`endif

`ifndef WARNING
`define WARNING(msg) \
    $display("WARNING: [%0t]: %s", $time, msg);
`endif

`ifndef ERROR
`define ERROR(msg) \
    $display("ERROR:   [%0t]: %s", $time, msg);
`endif

`define UNIT_TESTS \
    task automatic run();

`define UNIT_TEST(_TESTNAME_) \
    begin: _TESTNAME_ \
        setup();

`define UNIT_TEST_END \
    teardown(); \
    end

`define UNIT_TESTS_END endtask

`ifndef FAIL_IF
`define FAIL_IF(a) \
    if (a) \
        error = error + 1;
`endif

`ifndef FAIL_IF_EQUAL
`define FAIL_IF_EQUAL(a,b) \
    if (a === b) \
        error = error + 1;
`endif

`ifndef FAIL_IF_NOT_EQUAL
`define FAIL_IF_NOT_EQUAL(a,b) \
    if (a !== b) \
        error = error + 1;
`endif


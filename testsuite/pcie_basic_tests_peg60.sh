#!/bin/bash

echo "1.Running pcie_basic_tests.001_DATATRAFFIC_UPSTREAM_PEG60..."
echo "Parameters: PEG60, pcie_upstream_traffic_test, pcie_upstream_traffic_test, pcie_tests
"
perspec generate -define PCIE_NUM_CTRLS 1 -define PCIE_TEST_CTRL PEG60 -define CONTENT_REGRESSION_FLAG TRUE -define PCIE_TEST_CTRLS {PEG60} -f $MAESTRO_REPO_PATH/perspec/targets/adl_sil/adl_sil_tornado.psf -sln $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/pcie_tests.sln -top_action pcie_upstream_traffic_test -generate_test_table $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/pcie_tests.csv::pcie_upstream_traffic_test -target_dir pcie_upstream_traffic_test
MAESTRO_FRAMEWORK=UNIFIED CONTENT_TYPE=LINUX DEBUG=TRUE make -Bj TAGS=skl.qa -C ./pcie_upstream_traffic_test
$MAESTRO_REPO_PATH/build/content/linux/skl/root/pcie_automation/execution/pcie_upstream_traffic_test/pcie_upstream_traffic_test
echo "Completed"

echo "2.Running pcie_basic_tests.002_DATATRAFFIC_DOWNSTREAM_PEG60..."
echo "Parameters: PEG60, pcie_downstream_traffic_test, pcie_downstream_traffic_test, pcie_tests
"
perspec generate -define PCIE_NUM_CTRLS 1 -define PCIE_TEST_CTRL PEG60 -define CONTENT_REGRESSION_FLAG TRUE -define PCIE_TEST_CTRLS {PEG60} -f $MAESTRO_REPO_PATH/perspec/targets/adl_sil/adl_sil_tornado.psf -sln $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/pcie_tests.sln -top_action pcie_downstream_traffic_test -generate_test_table $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/pcie_tests.csv::pcie_downstream_traffic_test -target_dir pcie_downstream_traffic_test
MAESTRO_FRAMEWORK=UNIFIED CONTENT_TYPE=LINUX DEBUG=TRUE make -Bj TAGS=skl.qa -C ./pcie_downstream_traffic_test
$MAESTRO_REPO_PATH/build/content/linux/skl/root/pcie_automation/execution/pcie_downstream_traffic_test/pcie_downstream_traffic_test
echo "Completed"

echo "3.Running pcie_basic_tests.003_DATATRAFFIC_UPSTREAM_ATOMIC_SWAP_PEG60..."
echo "Parameters: PEG60, split_with_one_pattern_Atomics_SWAP, split_with_one_pattern, eden_test_table
"
perspec generate -define PCIE_NUM_CTRLS 1 -define PCIE_TEST_CTRL PEG60 -define CONTENT_REGRESSION_FLAG TRUE -define PCIE_TEST_CTRLS {PEG60} -f $MAESTRO_REPO_PATH/perspec/targets/adl_sil/adl_sil_tornado.psf -sln $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/eden_tc.sln -top_action split_with_one_pattern_Atomics_SWAP -generate_test_table $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/eden_test_table.csv::split_with_one_pattern -target_dir split_with_one_pattern_Atomics_SWAP
MAESTRO_FRAMEWORK=UNIFIED CONTENT_TYPE=LINUX DEBUG=TRUE make -Bj TAGS=skl.qa -C ./split_with_one_pattern_Atomics_SWAP
$MAESTRO_REPO_PATH/build/content/linux/skl/root/pcie_automation/execution/split_with_one_pattern_Atomics_SWAP/split_with_one_pattern_Atomics_SWAP
echo "Completed"

echo "4.Running pcie_basic_tests.004_DATA_TRAFFIC_UPSTREAM_ATOMIC_CAS_PEG60..."
echo "Parameters: PEG60, split_with_one_pattern_Atomics_CAS, split_with_one_pattern, eden_test_table
"
perspec generate -define PCIE_NUM_CTRLS 1 -define PCIE_TEST_CTRL PEG60 -define CONTENT_REGRESSION_FLAG TRUE -define PCIE_TEST_CTRLS {PEG60} -f $MAESTRO_REPO_PATH/perspec/targets/adl_sil/adl_sil_tornado.psf -sln $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/eden_tc.sln -top_action split_with_one_pattern_Atomics_CAS -generate_test_table $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/eden_test_table.csv::split_with_one_pattern -target_dir split_with_one_pattern_Atomics_CAS
MAESTRO_FRAMEWORK=UNIFIED CONTENT_TYPE=LINUX DEBUG=TRUE make -Bj TAGS=skl.qa -C ./split_with_one_pattern_Atomics_CAS
$MAESTRO_REPO_PATH/build/content/linux/skl/root/pcie_automation/execution/split_with_one_pattern_Atomics_CAS/split_with_one_pattern_Atomics_CAS
echo "Completed"

echo "5.Running pcie_basic_tests.005_DATA_TRAFFIC_UPSTREAM_ATOMIC_FETCHADD_PEG60..."
echo "Parameters: PEG60, split_with_one_pattern_Atomics_FETCHADD, split_with_one_pattern, eden_test_table
"
perspec generate -define PCIE_NUM_CTRLS 1 -define PCIE_TEST_CTRL PEG60 -define CONTENT_REGRESSION_FLAG TRUE -define PCIE_TEST_CTRLS {PEG60} -f $MAESTRO_REPO_PATH/perspec/targets/adl_sil/adl_sil_tornado.psf -sln $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/eden_tc.sln -top_action split_with_one_pattern_Atomics_FETCHADD -generate_test_table $MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/eden_test_table.csv::split_with_one_pattern -target_dir split_with_one_pattern_Atomics_FETCHADD
MAESTRO_FRAMEWORK=UNIFIED CONTENT_TYPE=LINUX DEBUG=TRUE make -Bj TAGS=skl.qa -C ./split_with_one_pattern_Atomics_FETCHADD
$MAESTRO_REPO_PATH/build/content/linux/skl/root/pcie_automation/execution/split_with_one_pattern_Atomics_FETCHADD/split_with_one_pattern_Atomics_FETCHADD
echo "Completed"

projectRoot = fileparts(mfilename('fullpath'));
addpath(fullfile(projectRoot, 'src'));
testsDir = fullfile(projectRoot, 'tests');

prefixFiles = dir(fullfile(testsDir, 'Test*.m'));
suffixFiles = dir(fullfile(testsDir, '*Test.m'));

% Merge and deduplicate by name
allFiles = [prefixFiles; suffixFiles];
[~, uniqueIdx] = unique({allFiles.name});
testFiles = allFiles(sort(uniqueIdx));

fprintf('Discovered %d test file(s) in %s\n', numel(testFiles), testsDir);
for i = 1:numel(testFiles)
    fprintf('  %s\n', testFiles(i).name);
end
fprintf('\n');

if numel(testFiles) == 0
    fprintf('No tests found.\n');
    exit(0);
end

suite = matlab.unittest.TestSuite.fromFile(fullfile(testFiles(1).folder, testFiles(1).name));
for i = 2:numel(testFiles)
    suite = [suite, matlab.unittest.TestSuite.fromFile(fullfile(testFiles(i).folder, testFiles(i).name))];
end

runner = matlab.unittest.TestRunner.withTextOutput( ...
    'Verbosity', matlab.unittest.Verbosity.Detailed);
results = runner.run(suite);

nTotal      = numel(results);
nPassed     = sum([results.Passed]);
nFailed     = sum([results.Failed]);
nIncomplete = sum([results.Incomplete]);
totalTime   = sum([results.Duration]);

fprintf('\n');
fprintf('========================================\n');
fprintf('  TEST SUMMARY\n');
fprintf('========================================\n');
fprintf('  Files:      %d\n', numel(testFiles));
fprintf('  Tests:      %d\n', nTotal);
fprintf('  Passed:     %d\n', nPassed);
fprintf('  Failed:     %d\n', nFailed);
fprintf('  Incomplete: %d\n', nIncomplete);
fprintf('  Duration:   %.3f s\n', totalTime);
fprintf('----------------------------------------\n');
if nFailed > 0 || nIncomplete > 0
    fprintf('  RESULT: FAILED\n');
    fprintf('========================================\n');
    exit(1);
else
    fprintf('  RESULT: ALL PASSED\n');
    fprintf('========================================\n');
    exit(0);
end

import React, { useState } from 'react';

export default function CodeEditor() {
  const [code, setCode] = useState(`function solution(input) {
  // Write your code here
  return input;
}`);
  const [output, setOutput] = useState('');
  const [selectedTest, setSelectedTest] = useState(0);

  const testCases = [
    {
      id: 1,
      name: 'Test Case 1: Add Two Numbers',
      input: '5, 3',
      expectedOutput: '8',
      description: 'Should return the sum of two numbers'
    },
    {
      id: 2,
      name: 'Test Case 2: Reverse String',
      input: '"hello"',
      expectedOutput: '"olleh"',
      description: 'Should return the reversed string'
    },
    {
      id: 3,
      name: 'Test Case 3: Array Sum',
      input: '[1, 2, 3, 4, 5]',
      expectedOutput: '15',
      description: 'Should return the sum of array elements'
    },
    {
      id: 4,
      name: 'Test Case 4: Is Even',
      input: '10',
      expectedOutput: 'true',
      description: 'Should return true if number is even'
    }
  ];

  const runCode = () => {
    try {
      setOutput('');
      const currentTest = testCases[selectedTest];
      
      // Parse the input
      let parsedInput;
      try {
        parsedInput = eval(currentTest.input);
      } catch {
        parsedInput = currentTest.input;
      }

      // Execute the user's code
      const userFunction = eval(`(${code})`);
      const result = userFunction(parsedInput);
      
      // Format output
      const resultStr = typeof result === 'string' ? `"${result}"` : String(result);
      const passed = resultStr === currentTest.expectedOutput;
      
      setOutput(`Input: ${currentTest.input}
Expected: ${currentTest.expectedOutput}
Got: ${resultStr}
Status: ${passed ? '✓ PASSED' : '✗ FAILED'}`);
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Code Editor</h1>
        <p style={styles.subtitle}>Write your solution and test it against different cases</p>
      </div>

      <div style={styles.content}>
        <div style={styles.leftPanel}>
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Test Cases</h3>
            <div style={styles.testList}>
              {testCases.map((test, index) => (
                <div
                  key={test.id}
                  style={{
                    ...styles.testItem,
                    ...(selectedTest === index ? styles.testItemActive : {})
                  }}
                  onClick={() => setSelectedTest(index)}
                >
                  <div style={styles.testName}>{test.name}</div>
                  <div style={styles.testDesc}>{test.description}</div>
                </div>
              ))}
            </div>
          </div>

          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Current Test Details</h3>
            <div style={styles.testDetails}>
              <div style={styles.detailRow}>
                <span style={styles.detailLabel}>Input:</span>
                <code style={styles.detailValue}>{testCases[selectedTest].input}</code>
              </div>
              <div style={styles.detailRow}>
                <span style={styles.detailLabel}>Expected:</span>
                <code style={styles.detailValue}>{testCases[selectedTest].expectedOutput}</code>
              </div>
            </div>
          </div>
        </div>

        <div style={styles.rightPanel}>
          <div style={styles.editorSection}>
            <div style={styles.editorHeader}>
              <h3 style={styles.sectionTitle}>Code Editor</h3>
              <button style={styles.runButton} onClick={runCode}>
                ▶ Run Test
              </button>
            </div>
            <textarea
              style={styles.editor}
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck={false}
            />
          </div>

          <div style={styles.outputSection}>
            <h3 style={styles.sectionTitle}>Output</h3>
            <pre style={styles.output}>{output || 'Run a test to see the output...'}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#2c3e50',
    color: 'white',
    padding: '20px 30px',
    borderBottom: '3px solid #3498db',
  },
  title: {
    margin: '0 0 5px 0',
    fontSize: '28px',
    fontWeight: '600',
  },
  subtitle: {
    margin: 0,
    fontSize: '14px',
    opacity: 0.9,
  },
  content: {
    display: 'flex',
    flex: 1,
    gap: '20px',
    padding: '20px',
    overflow: 'hidden',
  },
  leftPanel: {
    width: '350px',
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  rightPanel: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  section: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  sectionTitle: {
    margin: '0 0 15px 0',
    fontSize: '16px',
    fontWeight: '600',
    color: '#2c3e50',
  },
  testList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  testItem: {
    padding: '12px',
    borderRadius: '6px',
    border: '2px solid #e0e0e0',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  testItemActive: {
    borderColor: '#3498db',
    backgroundColor: '#e3f2fd',
  },
  testName: {
    fontWeight: '600',
    fontSize: '14px',
    marginBottom: '4px',
    color: '#2c3e50',
  },
  testDesc: {
    fontSize: '12px',
    color: '#7f8c8d',
  },
  testDetails: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  detailRow: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
  },
  detailLabel: {
    fontSize: '12px',
    fontWeight: '600',
    color: '#7f8c8d',
    textTransform: 'uppercase',
  },
  detailValue: {
    padding: '8px',
    backgroundColor: '#f8f9fa',
    borderRadius: '4px',
    fontSize: '14px',
    fontFamily: 'monospace',
  },
  editorSection: {
    flex: 1,
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
  },
  editorHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '15px',
  },
  runButton: {
    padding: '10px 20px',
    backgroundColor: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  editor: {
    flex: 1,
    fontFamily: '"Fira Code", "Courier New", monospace',
    fontSize: '14px',
    padding: '15px',
    border: '2px solid #e0e0e0',
    borderRadius: '6px',
    resize: 'none',
    outline: 'none',
    lineHeight: '1.6',
    backgroundColor: '#fafafa',
  },
  outputSection: {
    height: '200px',
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
  },
  output: {
    flex: 1,
    backgroundColor: '#1e1e1e',
    color: '#d4d4d4',
    padding: '15px',
    borderRadius: '6px',
    fontFamily: 'monospace',
    fontSize: '13px',
    margin: 0,
    overflow: 'auto',
    whiteSpace: 'pre-wrap',
  },
};
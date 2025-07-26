import React from 'react';
import { render, screen } from '@testing-library/react';

// Simple test to verify testing setup works
test('testing environment works', () => {
  expect(true).toBe(true);
});

test('basic React functionality works', () => {
  const TestComponent = () => <div>Test Component</div>;
  render(<TestComponent />);
  const element = screen.getByText('Test Component');
  expect(element).toBeInTheDocument();
});

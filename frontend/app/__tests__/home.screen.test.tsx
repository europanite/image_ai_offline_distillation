import { render, screen } from '@testing-library/react-native';

import HomeScreen from '../screens/HomeScreen';

describe('HomeScreen', () => {
  it('renders offline distillation controls', () => {
    render(<HomeScreen />);
    expect(screen.getByText('Image Offline Distillation')).toBeTruthy();
    expect(screen.getByText('1. Cache teacher logits')).toBeTruthy();
    expect(screen.getByText('2. Train student')).toBeTruthy();
    expect(screen.getByTestId('status').props.children).toBe('Ready.');
  });
});

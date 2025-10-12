import type { Meta, StoryObj } from '@storybook/nextjs-vite';
import Menu from './index';

const meta = {
  title: 'Components/Menu',
  component: Menu,
  parameters: {
    layout: 'padded',
    viewport: {
      defaultViewport: 'responsive',
    },
    docs: {
      story: {
        inline: false,
        iframeHeight: 600,
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    isOpen: {
      control: { type: 'boolean' },
      description: 'Controls whether the menu is visible',
    },
    onCancel: { 
      action: 'menu cancelled',
      description: 'Callback when background overlay is clicked',
    },
  },
} satisfies Meta<typeof Menu>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: (args) => <Menu {...args} />,
  args: {
    isOpen: true,
    onCancel: () => alert('Menu cancelled!'),
  },
};

export const Closed: Story = {
  render: (args) => <Menu {...args} />,
  args: {
    isOpen: false,
    onCancel: () => alert('Menu cancelled!'),
  },
};

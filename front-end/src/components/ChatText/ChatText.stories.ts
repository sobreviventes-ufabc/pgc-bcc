import type { Meta, StoryObj } from '@storybook/nextjs-vite';

import ChatText from './index';


const meta = {
  title: 'Components/ChatText',
  component: ChatText,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variation: {
      options: ['sent', 'received'],
      control: { type: 'radio' },
    },
    children: {
      control: 'text',
      description: 'Content of the chat message',
    },
  },
  args: {
    variation: 'sent',
    children: 'Hello, world!',
  },
} satisfies Meta<typeof ChatText>;

export default meta;
type Story = StoryObj<typeof meta>;


export const ChatTextStory: Story = {
  args: {
    variation: 'sent',
    children: 'Hello, world!',
  },
  globals: {
    backgrounds: { value: 'dark' },
  },
};

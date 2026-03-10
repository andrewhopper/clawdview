import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { apiEndpoints } from '@/lib/api';
import { RefreshCw, Send, Trash2, Plus } from 'lucide-react';

interface Item {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
}

export function HomePage() {
  const [greeting, setGreeting] = useState<string>('');
  const [items, setItems] = useState<Item[]>([]);
  const [newItemName, setNewItemName] = useState('');
  const [newItemDescription, setNewItemDescription] = useState('');
  const [chatInput, setChatInput] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadGreeting();
    loadItems();
  }, []);

  const loadGreeting = async () => {
    try {
      const data = await apiEndpoints.hello();
      setGreeting(data.message);
    } catch (err) {
      console.error('Failed to load greeting:', err);
    }
  };

  const loadItems = async () => {
    try {
      const data = await apiEndpoints.getItems();
      setItems(data.items as Item[]);
    } catch (err) {
      console.error('Failed to load items:', err);
    }
  };

  const createItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newItemName.trim()) return;

    setIsLoading(true);
    setError(null);
    try {
      await apiEndpoints.createItem({
        name: newItemName,
        description: newItemDescription || undefined,
      });
      setNewItemName('');
      setNewItemDescription('');
      await loadItems();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create item');
    } finally {
      setIsLoading(false);
    }
  };

  const deleteItem = async (id: string) => {
    setIsLoading(true);
    try {
      await apiEndpoints.deleteItem(id);
      await loadItems();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete item');
    } finally {
      setIsLoading(false);
    }
  };

  const sendChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    setIsLoading(true);
    setError(null);
    try {
      const response = await apiEndpoints.chat([
        { role: 'user', content: chatInput },
      ]);
      setChatResponse(response.content);
      setChatInput('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Greeting Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            Welcome
            <Button variant="ghost" size="icon" onClick={loadGreeting}>
              <RefreshCw className="h-4 w-4" />
            </Button>
          </CardTitle>
          <CardDescription>Response from the API</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-lg">{greeting || 'Loading...'}</p>
        </CardContent>
      </Card>

      {/* Items Section */}
      <Card>
        <CardHeader>
          <CardTitle>Items</CardTitle>
          <CardDescription>Manage your items (stored in DynamoDB)</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={createItem} className="flex gap-2">
            <Input
              placeholder="Item name"
              value={newItemName}
              onChange={(e) => setNewItemName(e.target.value)}
              className="flex-1"
            />
            <Input
              placeholder="Description (optional)"
              value={newItemDescription}
              onChange={(e) => setNewItemDescription(e.target.value)}
              className="flex-1"
            />
            <Button type="submit" disabled={isLoading || !newItemName.trim()}>
              <Plus className="h-4 w-4 mr-2" />
              Add
            </Button>
          </form>

          <div className="space-y-2">
            {items.length === 0 ? (
              <p className="text-muted-foreground text-sm">No items yet. Create one above!</p>
            ) : (
              items.map((item) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between p-3 rounded-lg border bg-card"
                >
                  <div>
                    <p className="font-medium">{item.name}</p>
                    {item.description && (
                      <p className="text-sm text-muted-foreground">{item.description}</p>
                    )}
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => deleteItem(item.id)}
                    disabled={isLoading}
                  >
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* AI Chat Section */}
      <Card>
        <CardHeader>
          <CardTitle>AI Chat</CardTitle>
          <CardDescription>Chat with Claude via AWS Bedrock</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={sendChat} className="flex gap-2">
            <Input
              placeholder="Ask something..."
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              className="flex-1"
            />
            <Button type="submit" disabled={isLoading || !chatInput.trim()}>
              <Send className="h-4 w-4 mr-2" />
              Send
            </Button>
          </form>

          {chatResponse && (
            <div className="p-4 rounded-lg bg-muted">
              <p className="whitespace-pre-wrap">{chatResponse}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Error Display */}
      {error && (
        <div className="p-4 rounded-lg bg-destructive/10 text-destructive">
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

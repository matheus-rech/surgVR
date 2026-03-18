using System.Collections.Generic;

[System.Serializable]
public class Wrapper<T>
{
    public List<T> items;
    public Wrapper(List<T> items) { this.items = items; }
}

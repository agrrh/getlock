export async function load({ fetch }) {
  const res = await fetch(
    `https://getlock.agrrh.com/api/v1/~demo`,
    {
      headers: {'X-Getlock-Auth': 'demo'},
    },
  );
  const data = await res.json();

  return data;
}

export function formatDate(iso) {
  if (!iso) return ''
  try {
    // Expect YYYY-MM-DD
    const [y, m, d] = iso.split('-')
    if (!y || !m || !d) return iso
    const date = new Date(`${iso}T00:00:00`)
    const monthName = date.toLocaleString('en-US', { month: 'long' })
    return `${y} ${monthName} ${Number(d)}`
  } catch {
    return iso
  }
}

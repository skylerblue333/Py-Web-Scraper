# Ecosystem Integration

**Role:** controlled external-data ingestion.

**Foundation:** Scrapy. Site-specific spiders must define explicit allowed domains and obey applicable terms, robots policies, and rate limits.

**Provides:** normalized source records to the data pipeline.

**Production requirements:** URL allowlists, concurrency limits, retries with backoff, content-size limits, deduplication, provenance, and telemetry.
